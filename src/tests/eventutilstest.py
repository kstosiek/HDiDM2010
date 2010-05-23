"""Unit test for eventutils.py"""

import eventutils 
import unittest

from new import function as make_function

def extract_function(func, subfunction_name):
	code = None
	for const in func.func_code.co_consts.__iter__():
		if hasattr(const, 'co_name') and const.co_name == subfunction_name:
			code = const
	return make_function(code, func.func_globals)

class EventUtilityFunctions(unittest.TestCase):

	def setUp(self):
		pass

	def testEventImport(self):
        	expected_result = ('category1', [ 
                      	(20090308, 20090308, 'event1'),
                       	(20090923, 20090925, 'event2'),
                       	(20090111, 20090111, 'event3')
                ])
	    	
		actual_result = eventutils.import_events("data/eventdata.txt")
        	self.assertEqual(actual_result, expected_result)

	def testDatesCollection(self):		
		collect_dates_function = extract_function(
			eventutils.trim_data_to_events, 'collect_dates')
		
		test_input = [ 
			[ 'company', { 20091101: 1, 20091102: 2 } ] 
		]
	
		expected_result = [ 20091101, 20091102 ]
		actual_result = collect_dates_function(test_input)

		self.assertEquals(actual_result, expected_result)

	def testEventDatesCollection(self):
		collect_event_dates_function = extract_function(
			eventutils.trim_data_to_events, 'collect_event_dates')
		

		test_input = { 
			'event_type_1': [ (20091101, 20091101, "desc1") ], 
			'event_type_2': [ (20091107, 20091108, "desc2") ]
		}

		expected_result = set([
			(20091101, 20091101),
			(20091107, 20091108)
		])

		actual_result = collect_event_dates_function(test_input)

		self.assertEquals(actual_result, expected_result)

	def testExpandByRange(self):
		expand_by_range_function = extract_function(
			eventutils.trim_data_to_events, 'expand_by_range')

		event_dates = set([
			(20091101, 20091101), 
			(20091103, 20091104),
                        (20091115, 20091115)
		])
		range = 3
		possible_dates = [
			20091101, 20091102, 20091103, 20091104, 20091105,
			20091108, 20091109, 20091110, 20091111, 20091112,
			20091115, 20091116
		]

		expected_result = set([
			20091101, 20091102, 20091103, 20091104, 20091105,
			20091108, 20091111, 20091112, 20091115, 20091116
		])

		actual_result = expand_by_range_function(
			event_dates, range, possible_dates)
		
		self.assertEquals(actual_result, expected_result)

	def testTrimmingDataToEventDates(self):
		trim_data_to_event_dates_function = extract_function(
			eventutils.trim_data_to_events, 
			'trim_data_to_event_dates')
		
		input_data = [
			[ 'company1', {
				20091101: 1, 20091102: 2, 20091103: 3,
				20091104: 4, 20091105: 5, 20091108: 6
			} ],
			[ 'company2', {
				20091101: 1, 20091102: 1, 20091103: 1,
				20091104: 1, 20091105: 1, 20091108: 1
			} ]		
		]
		event_dates = set([ 20091101, 20091108 ])
		
		expected_result = [ 
			[ 'company1', { 20091101: 1, 20091108: 6 } ],
			[ 'company2', { 20091101: 1, 20091108: 1 } ]
		]

		actual_result = trim_data_to_event_dates_function(
			input_data, event_dates)
		
		self.assertEquals(actual_result, expected_result)


	def testTrimDataToEvents(self):
		test_data = [
			[ 'company1', {
				20091101: 1, 20091102: 2, 20091103: 3,
				20091104: 4, 20091105: 5, 20091108: 6
			} ],
			[ 'company2', {
				20091101: 1, 20091102: 1, 20091103: 1,
				20091104: 1, 20091105: 1, 20091108: 1
			} ]		
		]

		test_events = { 
			'event_type_1': [ (20091101, 20091101, "desc1") ], 
			'event_type_2': [ (20091107, 20091108, "desc2") ]
		}

		range = 2

		expected_result = [
			[ 'company1', { 
				20091101: 1, 20091102: 2,
				20091104: 4, 20091105: 5, 20091108: 6
			} ],
			[ 'company2', {
				20091101: 1, 20091102: 1,
				20091104: 1, 20091105: 1, 20091108: 1
			}]
		]

		actual_result = eventutils.trim_data_to_events(
			test_data, test_events, range)

		self.assertEquals(actual_result, expected_result)


if __name__ == "__main__":
	unittest.main()

