from bt2 import values
import unittest
import copy
import bt2


class EventClassTestCase(unittest.TestCase):
    def setUp(self):
        self._context_ft = bt2.StructureFieldType()
        self._context_ft.append_field('allo', bt2.StringFieldType())
        self._context_ft.append_field('zola', bt2.IntegerFieldType(18))
        self._payload_ft = bt2.StructureFieldType()
        self._payload_ft.append_field('zoom', bt2.StringFieldType())
        self._ec = bt2.EventClass('my_event')
        self._ec.id = 18
        self._ec.context_field_type = self._context_ft
        self._ec.payload_field_type = self._payload_ft

    def test_create(self):
        self.assertEqual(self._ec.name, 'my_event')
        self.assertEqual(self._ec.id, 18)
        self.assertEqual(self._ec.context_field_type, self._context_ft)
        self.assertEqual(self._ec.payload_field_type, self._payload_ft)

    def test_create_invalid_no_name(self):
        with self.assertRaises(TypeError):
            bt2.EventClass()

    def test_create_full(self):
        ec = bt2.EventClass(name='name', id=23,
                            context_field_type=self._context_ft,
                            payload_field_type=self._payload_ft,
                            attributes={'model.emf.uri': 'my URI'})
        self.assertEqual(ec.name, 'name')
        self.assertEqual(ec.id, 23)
        self.assertEqual(ec.context_field_type, self._context_ft)
        self.assertEqual(ec.payload_field_type, self._payload_ft)
        self.assertEqual(ec.attributes['model.emf.uri'], 'my URI')

    def test_assign_id(self):
        self._ec.id = 1717
        self.assertEqual(self._ec.id, 1717)

    def test_assign_invalid_id(self):
        with self.assertRaises(TypeError):
            self._ec.id = 'lel'

    def test_assign_context_field_type(self):
        self._ec.context_field_type = self._payload_ft
        self.assertEqual(self._ec.context_field_type, self._payload_ft)

    def test_assign_no_context_field_type(self):
        self._ec.context_field_type = None
        self.assertIsNone(self._ec.context_field_type)

    def test_assign_invalid_context_field_type(self):
        with self.assertRaises(TypeError):
            self._ec.context_field_type = 'lel'

    def test_assign_payload_field_type(self):
        self._ec.payload_field_type = self._payload_ft
        self.assertEqual(self._ec.payload_field_type, self._payload_ft)

    def test_assign_no_payload_field_type(self):
        self._ec.payload_field_type = None
        self.assertIsNone(self._ec.payload_field_type)

    def test_assign_invalid_payload_field_type(self):
        with self.assertRaises(TypeError):
            self._ec.payload_field_type = 'lel'

    def test_stream_class_prop_no_sc(self):
        self.assertIsNone(self._ec.stream_class)

    def test_stream_class_prop(self):
        sc = bt2.StreamClass()
        sc.add_event_class(self._ec)
        self.assertEqual(self._ec.stream_class.addr, sc.addr)

    def _test_copy(self, cpy):
        self.assertIsNot(cpy, self._ec)
        self.assertNotEqual(cpy.addr, self._ec.addr)
        self.assertEqual(cpy, self._ec)

    def test_copy(self):
        cpy = copy.copy(self._ec)
        self._test_copy(cpy)
        self.assertEqual(self._ec.context_field_type.addr, cpy.context_field_type.addr)
        self.assertEqual(self._ec.payload_field_type.addr, cpy.payload_field_type.addr)

    def test_deepcopy(self):
        cpy = copy.deepcopy(self._ec)
        self._test_copy(cpy)
        self.assertNotEqual(self._ec.context_field_type.addr, cpy.context_field_type.addr)
        self.assertNotEqual(self._ec.payload_field_type.addr, cpy.payload_field_type.addr)

    def test_attr_getitem(self):
        self.assertEqual(self._ec.attributes['id'], 18)
        self.assertEqual(self._ec.attributes['name'], 'my_event')

    def test_attr_setitem(self):
        self._ec.attributes['model.emf.uri'] = 'my url'
        self.assertEqual(self._ec.attributes['model.emf.uri'], 'my url')

    def test_attr_len(self):
        self.assertTrue(len(self._ec.attributes) != 0)

    def test_attr_iter(self):
        for name, value in self._ec.attributes.items():
            self.assertIsInstance(value, values._Value)

            if name == 'name':
                self.assertEqual(value, 'my_event')
            elif name == 'id':
                self.assertEqual(value, 18)

    def test_eq(self):
        ec1 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        ec2 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        self.assertEqual(ec1, ec2)

    def test_ne_name(self):
        ec1 = bt2.EventClass(name='name1', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        ec2 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        self.assertNotEqual(ec1, ec2)

    def test_ne_id(self):
        ec1 = bt2.EventClass(name='name', id=24,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        ec2 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        self.assertNotEqual(ec1, ec2)

    def test_ne_context_field_type(self):
        ec1 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._payload_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        ec2 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        self.assertNotEqual(ec1, ec2)

    def test_ne_payload_field_type(self):
        ec1 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._context_ft,
                             attributes={'model.emf.uri': 'my URI'})
        ec2 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        self.assertNotEqual(ec1, ec2)

    def test_ne_attribute(self):
        ec1 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my URI'})
        ec2 = bt2.EventClass(name='name', id=23,
                             context_field_type=self._context_ft,
                             payload_field_type=self._payload_ft,
                             attributes={'model.emf.uri': 'my UR'})
        self.assertNotEqual(ec1, ec2)

    def test_eq_invalid(self):
        self.assertFalse(self._ec == 23)
