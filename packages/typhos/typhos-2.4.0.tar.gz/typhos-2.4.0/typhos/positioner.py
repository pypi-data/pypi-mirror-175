import logging
import os.path
import threading

from pydm.widgets.channel import PyDMChannel
from qtpy import QtCore, QtWidgets, uic

from . import utils, widgets
from .alarm import KindLevel, _KindLevel
from .status import TyphosStatusThread

logger = logging.getLogger(__name__)


class TyphosPositionerWidget(
    utils.TyphosBase,
    widgets.TyphosDesignerMixin,
    _KindLevel,
):
    """
    Widget to interact with a :class:`ophyd.Positioner`.

    Standard positioner motion requires a large amount of context for
    operators. For most motors, it may not be enough to simply have a text
    field where setpoints can be punched in. Instead, information like soft
    limits and hardware limit switches are crucial for a full understanding of
    the position and behavior of a motor. The widget will work with any object
    that implements the method ``set``, however to get other relevant
    information, we see if we can find other useful signals.  Below is a table
    of attributes that the widget looks for to inform screen design.

    ============== ===========================================================
    Widget         Attribute Selection
    ============== ===========================================================
    User Readback  The ``readback_attribute`` property is used, which defaults
                   to ``user_readback``. Linked to UI element
                   ``user_readback``.

    User Setpoint  The ``setpoint_attribute`` property is used, which defaults
                   to ``user_setpoint``. Linked to UI element
                   ``user_setpoint``.

    Limit Switches The ``low_limit_switch_attribute`` and
                   ``high_limit_switch_attribute`` properties are used, which
                   default to ``low_limit_switch`` and ``high_limit_switch``,
                   respectively.

    Soft Limits    The ``low_limit_travel_attribute`` and
                   ``high_limit_travel_attribute`` properties are used, which
                   default to ``low_limit_travel`` and ``high_limit_travel``,
                   respectively.  As a fallback, the ``limit`` property on the
                   device may be queried directly.

    Set and Tweak  Both of these methods simply use ``Device.set`` which is
                   expected to take a ``float`` and return a ``status`` object
                   that indicates the motion completeness. Must be implemented.

    Stop           ``Device.stop()``, if available, otherwise hide the button.
                   If you have a non-functional ``stop`` method inherited from
                   a parent device, you can hide it from ``typhos`` by
                   overriding it with a property that raises
                   ``AttributeError`` on access.

    Move Indicator The ``moving_attribute`` property is used, which defaults
                   to ``motor_is_moving``. Linked to UI element
                   ``moving_indicator``.

    Error Message  The ``error_message_attribute`` property is used, which
                   defaults to ``error_message``. Linked to UI element
                   ``error_label``.

    Clear Error    ``Device.clear_error()``, if applicable. This also clears
                   any visible error messages from the status returned by
                   ``Device.set``.

    Alarm Circle   Uses the ``TyphosAlarmCircle`` widget to summarize the
                   alarm state of all of the device's ``normal`` and
                   ``hinted`` signals.
    ============== ===========================================================
    """
    QtCore.Q_ENUMS(_KindLevel)
    KindLevel = KindLevel

    ui_template = os.path.join(utils.ui_dir, 'widgets', 'positioner.ui')
    _readback_attr = 'user_readback'
    _setpoint_attr = 'user_setpoint'
    _low_limit_switch_attr = 'low_limit_switch'
    _high_limit_switch_attr = 'high_limit_switch'
    _low_limit_travel_attr = 'low_limit_travel'
    _high_limit_travel_attr = 'high_limit_travel'
    _velocity_attr = 'velocity'
    _acceleration_attr = 'acceleration'
    _moving_attr = 'motor_is_moving'
    _error_message_attr = 'error_message'
    _min_visible_operation = 0.1

    def __init__(self, parent=None):
        self._moving = False
        self._last_move = None
        self._readback = None
        self._setpoint = None
        self._status_thread = None
        self._initialized = False
        self._moving_channel = None

        super().__init__(parent=parent)

        self.ui = uic.loadUi(self.ui_template, self)
        self.ui.tweak_positive.clicked.connect(self.positive_tweak)
        self.ui.tweak_negative.clicked.connect(self.negative_tweak)
        self.ui.stop_button.clicked.connect(self.stop)
        self.ui.clear_error_button.clicked.connect(self.clear_error)

        self.ui.alarm_circle.kindLevel = self.ui.alarm_circle.NORMAL
        self.ui.alarm_circle.alarm_changed.connect(self.update_alarm_text)

        self.show_expert_button = False
        self._after_set_moving(False)

    def _clear_status_thread(self):
        """Clear a previous status thread."""
        if self._status_thread is None:
            return

        logger.debug("Clearing current active status")
        self._status_thread.disconnect()
        self._status_thread = None

    def _start_status_thread(self, status, timeout):
        """Start the status monitoring thread for the given status object."""
        self._status_thread = thread = TyphosStatusThread(
            status, start_delay=self._min_visible_operation,
            timeout=timeout,
            parent=self,
        )
        thread.status_started.connect(self.move_changed)
        thread.status_finished.connect(self._status_finished)
        thread.start()

    def _get_timeout(self, set_position, settle_time):
        """Use positioner's configuration to select a timeout."""
        pos_sig = getattr(self.device, self._readback_attr, None)
        vel_sig = getattr(self.device, self._velocity_attr, None)
        acc_sig = getattr(self.device, self._acceleration_attr, None)
        # Not enough info == no timeout
        if pos_sig is None or vel_sig is None:
            return None
        delta = pos_sig.get() - set_position
        speed = vel_sig.get()
        # Bad speed == no timeout
        if speed == 0:
            return None
        # Bad acceleration == ignore acceleration
        if acc_sig is None:
            acc_time = 0
        else:
            acc_time = acc_sig.get()
        # This time is always greater than the kinematic calc
        return abs(delta/speed) + 2 * abs(acc_time) + abs(settle_time)

    def _set(self, value):
        """Inner `set` routine - call device.set() and monitor the status."""
        self._clear_status_thread()
        self._last_move = None
        if isinstance(self.ui.set_value, widgets.NoScrollComboBox):
            set_position = value
        else:
            set_position = float(value)

        try:
            timeout = self._get_timeout(set_position, 5)
        except Exception:
            # Something went wrong, just run without a timeout.
            logger.exception('Unable to estimate motor timeout.')
            timeout = None
        logger.debug("Setting device %r to %r with timeout %r",
                     self.device, value, timeout)
        try:
            status = self.device.set(set_position)
        except Exception as exc:
            # Treat this exception as a status to use normal error reporting
            # Usually this is e.g. limits error
            self._status_finished(exc)
        else:
            # Send timeout through thread because status timeout stops the move
            self._start_status_thread(status, timeout)

    @QtCore.Slot(int)
    def combo_set(self, index):
        self.set()

    @QtCore.Slot()
    def set(self):
        """Set the device to the value configured by ``ui.set_value``"""
        if not self.device:
            return

        try:
            if isinstance(self.ui.set_value, widgets.NoScrollComboBox):
                value = self.ui.set_value.currentText()
            else:
                value = self.ui.set_value.text()
            self._set(value)
        except Exception as exc:
            logger.exception("Error setting %r to %r", self.devices, value)
            self._last_move = False
            utils.reload_widget_stylesheet(self, cascade=True)
            utils.raise_to_operator(exc)

    def tweak(self, offset):
        """Tweak by the given ``offset``."""
        try:
            setpoint = self._get_position() + float(offset)
        except Exception:
            logger.exception('Tweak failed')
            return

        self.ui.set_value.setText(str(setpoint))
        self.set()

    @QtCore.Slot()
    def positive_tweak(self):
        """Tweak positive by the amount listed in ``ui.tweak_value``"""
        try:
            self.tweak(float(self.tweak_value.text()))
        except Exception:
            logger.exception('Tweak failed')

    @QtCore.Slot()
    def negative_tweak(self):
        """Tweak negative by the amount listed in ``ui.tweak_value``"""
        try:
            self.tweak(-float(self.tweak_value.text()))
        except Exception:
            logger.exception('Tweak failed')

    @QtCore.Slot()
    def stop(self):
        """Stop device"""
        for device in self.devices:
            # success=True means expected stop
            device.stop(success=True)

    @QtCore.Slot()
    def clear_error(self):
        """
        Clear the error messages from the device and screen.

        The device may have errors in the IOC. These will be cleared by calling
        the clear_error method.

        The screen may have errors from the status of the last move. These will
        be cleared from view.
        """
        for device in self.devices:
            clear_error_in_background(device)
        self._set_status_text('')
        # This variable holds True if last move was good, False otherwise
        # It also controls whether or not we have a red box on the widget
        # False = Red, True = Green, None = no box (in motion is yellow)
        if not self._last_move:
            self._last_move = None
        utils.reload_widget_stylesheet(self, cascade=True)

    def _get_position(self):
        if not self._readback:
            raise Exception("No Device configured for widget!")
        return self._readback.get()

    @utils.linked_attribute('readback_attribute', 'ui.user_readback', True)
    def _link_readback(self, signal, widget):
        """Link the positioner readback with the ui element."""
        self._readback = signal

    @utils.linked_attribute('setpoint_attribute', 'ui.user_setpoint', True)
    def _link_setpoint(self, signal, widget):
        """Link the positioner setpoint with the ui element."""
        self._setpoint = signal
        if signal is not None:
            # Seed the set_value text with the user_setpoint channel value.
            if hasattr(widget, 'textChanged'):
                widget.textChanged.connect(self._user_setpoint_update)

    @utils.linked_attribute('low_limit_switch_attribute',
                            'ui.low_limit_switch', True)
    def _link_low_limit_switch(self, signal, widget):
        """Link the positioner lower limit switch with the ui element."""
        if signal is None:
            widget.hide()

    @utils.linked_attribute('high_limit_switch_attribute',
                            'ui.high_limit_switch', True)
    def _link_high_limit_switch(self, signal, widget):
        """Link the positioner high limit switch with the ui element."""
        if signal is None:
            widget.hide()

    @utils.linked_attribute('low_limit_travel_attribute', 'ui.low_limit', True)
    def _link_low_travel(self, signal, widget):
        """Link the positioner lower travel limit with the ui element."""
        return signal is not None

    @utils.linked_attribute('high_limit_travel_attribute', 'ui.high_limit',
                            True)
    def _link_high_travel(self, signal, widget):
        """Link the positioner high travel limit with the ui element."""
        return signal is not None

    def _link_limits_by_limits_attr(self):
        """Link limits by using ``device.limits``."""
        device = self.device
        try:
            low_limit, high_limit = device.limits
        except Exception:
            ...
        else:
            if low_limit < high_limit:
                self.ui.low_limit.setText(str(low_limit))
                self.ui.high_limit.setText(str(high_limit))
                return

        # If not found or invalid, hide them:
        self.ui.low_limit.hide()
        self.ui.high_limit.hide()

    @utils.linked_attribute('moving_attribute', 'ui.moving_indicator', True)
    def _link_moving(self, signal, widget):
        """Link the positioner moving indicator with the ui element."""
        if signal is None:
            widget.hide()
            return False
        widget.show()
        # Additional handling for updating self.moving
        if self._moving_channel is not None:
            self._moving_channel.disconnect()
        chname = utils.channel_from_signal(signal)
        self._moving_channel = PyDMChannel(
            address=chname,
            value_slot=self._set_moving,
            )
        self._moving_channel.connect()
        return True

    @utils.linked_attribute('error_message_attribute', 'ui.error_label', True)
    def _link_error_message(self, signal, widget):
        """Link the IOC error message with the ui element."""
        if signal is None:
            widget.hide()

    def _define_setpoint_widget(self):
        """
        Leverage information at describe to define whether to use a
        PyDMLineEdit or a PyDMEnumCombobox as setpoint widget.
        """
        try:
            setpoint_signal = getattr(self.device, self.setpoint_attribute)
            selection = setpoint_signal.enum_strs is not None
        except Exception:
            selection = False

        if selection:
            self.ui.set_value = widgets.NoScrollComboBox()
            self.ui.set_value.addItems(setpoint_signal.enum_strs)
            # Activated signal triggers only when the user selects an option
            self.ui.set_value.activated.connect(self.set)
            self.ui.set_value.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Fixed,
                )
            self.ui.set_value.setMinimumContentsLength(20)
            self.ui.tweak_widget.setVisible(False)
        else:
            self.ui.set_value = QtWidgets.QLineEdit()
            self.ui.set_value.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.set_value.returnPressed.connect(self.set)

        self.ui.setpoint_layout.addWidget(self.ui.set_value)

    @property
    def device(self):
        """The associated device."""
        try:
            return self.devices[0]
        except Exception:
            ...

    def add_device(self, device):
        """Add a device to the widget"""
        # Add device to cache
        self.devices.clear()  # only one device allowed
        super().add_device(device)

        self._define_setpoint_widget()
        self._link_readback()
        self._link_setpoint()
        self._link_low_limit_switch()
        self._link_high_limit_switch()

        # If the stop method is missing, hide the button
        try:
            device.stop
            self.ui.stop_button.show()
        except AttributeError:
            self.ui.stop_button.hide()

        if not (self._link_low_travel() and self._link_high_travel()):
            self._link_limits_by_limits_attr()

        if self._link_moving():
            self.ui.moving_indicator_label.show()
        else:
            self.ui.moving_indicator_label.hide()

        self._link_error_message()

        if self.show_expert_button:
            self.ui.expert_button.devices.clear()
            self.ui.expert_button.add_device(device)

        self.ui.alarm_circle.clear_all_alarm_configs()
        self.ui.alarm_circle.add_device(device)

    @QtCore.Property(bool, designable=False)
    def moving(self):
        """
        Current state of widget

        This will lag behind the actual state of the positioner in order to
        prevent unnecessary rapid movements
        """
        return self._moving

    @moving.setter
    def moving(self, value):
        if value != self._moving:
            self._moving = value
            self._after_set_moving(value)

    def _after_set_moving(self, value):
        """
        Common updates needed after a change to the moving state.

        This is pulled out as a separate method because we need
        to initialize the label here during __init__ without
        modifying self.moving.
        """
        utils.reload_widget_stylesheet(self, cascade=True)
        if value:
            self.ui.moving_indicator_label.setText('moving')
        else:
            self.ui.moving_indicator_label.setText('done')

    def _set_moving(self, value):
        """
        Slot for updating the self.moving property.

        This is used e.g. in updating the moving state when the
        motor starts moving in EPICS but not by the request of
        this widget.
        """
        self.moving = bool(value)

    @QtCore.Property(bool, designable=False)
    def successful_move(self):
        """The last requested move was successful"""
        return self._last_move is True

    @QtCore.Property(bool, designable=False)
    def failed_move(self):
        """The last requested move failed"""
        return self._last_move is False

    @QtCore.Property(str, designable=True)
    def readback_attribute(self):
        """The attribute name for the readback signal."""
        return self._readback_attr

    @readback_attribute.setter
    def readback_attribute(self, value):
        self._readback_attr = value

    @QtCore.Property(str, designable=True)
    def setpoint_attribute(self):
        """The attribute name for the setpoint signal."""
        return self._setpoint_attr

    @setpoint_attribute.setter
    def setpoint_attribute(self, value):
        self._setpoint_attr = value

    @QtCore.Property(str, designable=True)
    def low_limit_switch_attribute(self):
        """The attribute name for the low limit switch signal."""
        return self._low_limit_switch_attr

    @low_limit_switch_attribute.setter
    def low_limit_switch_attribute(self, value):
        self._low_limit_switch_attr = value

    @QtCore.Property(str, designable=True)
    def high_limit_switch_attribute(self):
        """The attribute name for the high limit switch signal."""
        return self._high_limit_switch_attr

    @high_limit_switch_attribute.setter
    def high_limit_switch_attribute(self, value):
        self._high_limit_switch_attr = value

    @QtCore.Property(str, designable=True)
    def low_limit_travel_attribute(self):
        """The attribute name for the low limit signal."""
        return self._low_limit_travel_attr

    @low_limit_travel_attribute.setter
    def low_limit_travel_attribute(self, value):
        self._low_limit_travel_attr = value

    @QtCore.Property(str, designable=True)
    def high_limit_travel_attribute(self):
        """The attribute name for the high (soft) limit travel signal."""
        return self._high_limit_travel_attr

    @high_limit_travel_attribute.setter
    def high_limit_travel_attribute(self, value):
        self._high_limit_travel_attr = value

    @QtCore.Property(str, designable=True)
    def velocity_attribute(self):
        """The attribute name for the velocity signal."""
        return self._velocity_attr

    @velocity_attribute.setter
    def velocity_attribute(self, value):
        self._velocity_attr = value

    @QtCore.Property(str, designable=True)
    def acceleration_attribute(self):
        """The attribute name for the acceleration time signal."""
        return self._acceleration_attr

    @acceleration_attribute.setter
    def acceleration_attribute(self, value):
        self._acceleration_attr = value

    @QtCore.Property(str, designable=True)
    def moving_attribute(self):
        """The attribute name for the motor moving indicator."""
        return self._moving_attr

    @moving_attribute.setter
    def moving_attribute(self, value):
        self._moving_attr = value

    @QtCore.Property(str, designable=True)
    def error_message_attribute(self):
        """The attribute name for the IOC error message label."""
        return self._error_message_attr

    @error_message_attribute.setter
    def error_message_attribute(self, value):
        self._error_message_attr = value

    @QtCore.Property(bool, designable=True)
    def show_expert_button(self):
        """
        If True, show the expert button.

        The expert button opens a full suite for the device.
        You typically want this False when you're already inside the
        suite that the button would open.
        You typically want this True when you're using the positioner widget
        inside of an unrelated screen.
        This will default to False.
        """
        return self._show_expert_button

    @show_expert_button.setter
    def show_expert_button(self, show):
        self._show_expert_button = show
        if show:
            self.ui.expert_button.show()
        else:
            self.ui.expert_button.hide()

    @QtCore.Property(_KindLevel, designable=True)
    def alarmKindLevel(self) -> KindLevel:
        return self.ui.alarm_circle.kindLevel

    @alarmKindLevel.setter
    def alarmKindLevel(self, kind_level: KindLevel):
        if kind_level != self.alarmKindLevel:
            self.ui.alarm_circle.kindLevel = kind_level

    def move_changed(self):
        """Called when a move is begun"""
        logger.debug("Begin showing move in TyphosPositionerWidget")
        self.moving = True

    def _set_status_text(self, text, *, max_length=60):
        """Set the status text label to ``text``."""
        if len(text) >= max_length:
            self.ui.status_label.setToolTip(text)
            text = text[:max_length] + '...'
        else:
            self.ui.status_label.setToolTip('')

        self.ui.status_label.setText(text)

    def _status_finished(self, result):
        """Called when a move is complete."""
        if isinstance(result, Exception):
            text = f'<b>{result.__class__.__name__}</b> {result}'
        else:
            text = ''

        self._set_status_text(text)

        success = not isinstance(result, Exception)
        logger.debug("Completed move in TyphosPositionerWidget (result=%r)",
                     result)
        self._last_move = success
        self.moving = False

    @QtCore.Slot(str)
    def _user_setpoint_update(self, text):
        """Qt slot - indicating the ``user_setpoint`` widget text changed."""
        try:
            text = text.strip().split(' ')[0]
            text = text.strip()
        except Exception:
            return

        # Update set_value if it's not being edited.
        if not self.ui.set_value.hasFocus():
            if isinstance(self.ui.set_value, widgets.NoScrollComboBox):
                try:
                    idx = int(text)
                    self.ui.set_value.setCurrentIndex(idx)
                    self._initialized = True
                except ValueError:
                    logger.debug('Failed to convert value to int. %s', text)
            else:
                self._initialized = True
                self.ui.set_value.setText(text)

    def update_alarm_text(self, alarm_level):
        """
        Label the alarm circle with a short text bit.
        """
        alarms = self.ui.alarm_circle.AlarmLevel
        if alarm_level == alarms.NO_ALARM:
            text = 'no alarm'
        elif alarm_level == alarms.MINOR:
            text = 'minor'
        elif alarm_level == alarms.MAJOR:
            text = 'major'
        elif alarm_level == alarms.DISCONNECTED:
            text = 'no conn'
        else:
            text = 'invalid'
        self.ui.alarm_label.setText(text)


def clear_error_in_background(device):
    def inner():
        try:
            device.clear_error()
        except AttributeError:
            pass
        except Exception:
            msg = "Could not clear error!"
            logger.error(msg)
            logger.debug(msg, exc_info=True)

    td = threading.Thread(target=inner)
    td.start()
