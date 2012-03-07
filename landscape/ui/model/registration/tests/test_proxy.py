import dbus

from landscape.tests.helpers import LandscapeTest
from landscape.ui.tests.helpers import (
    got_gobject_introspection, gobject_skip_message)
if got_gobject_introspection:
    from landscape.ui.model.registration.mechanism import (
        RegistrationMechanism, INTERFACE_NAME)
    from landscape.ui.model.registration.proxy import RegistrationProxy


class RegistrationProxyTest(LandscapeTest):
    """
    L{RegistrationProxyTest} bypasses DBus to simply check the interface
    between the proxy and the mechanism it would usually contact via DBus.
    """

    def setUp(self):
        super(RegistrationProxyTest, self).setUp()
        bus_name = dbus.service.BusName(INTERFACE_NAME,
                                        RegistrationProxyTest.bus)

        def fake_do__registration(this, config_path):
            return True

        def fake_do__disabling(this):
            return True

        RegistrationMechanism._do_registration = fake_do__registration
        RegistrationMechanism._do_disabling = fake_do__disabling
        self.mechanism = RegistrationMechanism(bus_name)

        def fake_setup_interface(this, bus):
            """
            This just allows us to test without actually relying on dbus.
            """
            this._interface = self.mechanism

        def fake_register_handlers(this):
            pass

        def fake_remove_handlers(this):
            pass

        def fake_callback(message):
            pass

        RegistrationProxy._setup_interface = fake_setup_interface
        RegistrationProxy._register_handlers = fake_register_handlers
        RegistrationProxy._remove_handlers = fake_remove_handlers
        self.proxy = RegistrationProxy(fake_callback, fake_callback,
                                       fake_callback, fake_callback,
                                       fake_callback, fake_callback)

    def tearDown(self):
        self.mechanism.remove_from_connection()
        super(RegistrationProxyTest, self).tearDown()

    def test_register(self):
        """
        Test that the proxy calls through to the underlying interface and
        correctly performs registration.
        """
        self.assertEqual((True, "Connected\n"), self.proxy.register("foo"))

    def test_disable(self):
        """
        Test that the proxy calls through to the underlying interface and
        correctly performs disabling.
        """
        self.assertEqual(True, self.proxy.disable())

    if not got_gobject_introspection:
        skip = gobject_skip_message
    else:
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        try:
            bus = dbus.SessionBus(private=True)
        except dbus.exceptions.DBusException:
            test_register.skip = ("Cannot launch private DBus session without "
                                  "X11")