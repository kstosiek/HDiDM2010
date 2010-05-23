def import_events(event_file_name):
        def get_category_name(file):
                return file.readline().rstrip('\n')

        def get_events(file):
                events = [ ]
                for line in file:
                        start_date, end_date, description = line.split(';')
                        events.append((
                                int(start_date),
                                int(end_date),
                                description.rstrip('\n')
                        ))
                return events

        file = open(event_file_name, 'r')
        category = get_category_name(file)
        events = get_events(file)
        file.close()

        return (category, events)

def trim_data_to_events(data, events, range):
        def collect_dates(data):
                # We assume that dates are the same for each compay.
                company, prices_by_date = data[0]
                return prices_by_date.keys()

        def collect_event_dates(events):
                event_dates = []
                for event_type, event_details in events.iteritems():
                        for start_date, end_date, description in event_details:
                                event_dates.append((start_date, end_date))
                return set(event_dates)

        def expand_by_range(event_dates, range, possible_dates):
                def expand_left(date, range, possible_dates):
                        dates_to_collect = range
                        current_date = date
                        dates_collected = []

                        while dates_to_collect > 0:
                                if current_date in possible_dates:
                                        dates_collected.append(current_date)
                                        dates_to_collect -= 1
                                current_date -= 1
                                if current_date < possible_dates[0]:
                                        break

                        return dates_collected


                def expand_right(date, range, possible_dates):
                        dates_to_collect = range
                        current_date = date
                        dates_collected = []

                        while dates_to_collect > 0:
                                if current_date in possible_dates:
                                        dates_collected.append(current_date)
                                        dates_to_collect -= 1
                                current_date += 1
                                if current_date > possible_dates[len(possible_dates) - 1]:
                                        break

                        return dates_collected

                expansion_result = []
                for start_date, end_date in event_dates:
                        expansion_result.extend(expand_left(start_date, range, possible_dates))
                        expansion_result.extend(expand_right(end_date, range, possible_dates))
                return set(expansion_result)




        def trim_data_to_event_dates(data, event_dates):
                def trim_prices_by_date(prices_by_date, event_dates):
                        trimmed_prices_by_date = { }
                        for event_date in event_dates:
                                trimmed_prices_by_date[event_date] = prices_by_date[event_date]
                        return trimmed_prices_by_date

                trimmed_data = []
                for company, prices_by_date in data:
                        trimmed_data.append([
                                company,
                                trim_prices_by_date(prices_by_date, event_dates)
                        ]
)
                return trimmed_data


        all_dates = collect_dates(data)
        all_dates.sort()

        event_dates = collect_event_dates(events)
        event_dates = expand_by_range(event_dates, range, all_dates)

        return trim_data_to_event_dates(data, event_dates)


if __name__ == "__main__":
        data = parse_data("../data/notowania.txt")
        events = import_events("../data/wydarzenia-inne-polska.txt")
        event_map = { events[0]: events[1] }
        for company, prices_by_date in trim_data_to_events(data, event_map, 5):
                print company
                for date in prices_by_date.keys():
                        print date, ': ', prices_by_date[date]
        trim_data_to_events.trim_data_to_event_dates(None, None)

