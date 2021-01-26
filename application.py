# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import wowapi as wapi
import db_access as awsdb
import db_schema
import db_functions
import schedule


def recurring_task():
    token = wapi.create_access_token('6440de7fe7f7433fb9a4d07981e88ff3', 'LSsT215b5G0uOhr66MlWU5U5imuUXmai')
    output_list = wapi.retrieve_auctions(token)

    blizz_ah = wapi.clean_data(output_list)

    awsdb.connect()
    db_schema.create_tables()

    id_list = [171276, 171315, 168586, 168589, 168583, 170554, 171278]
    blizz_ah_clean = db_functions.filter_auctions(id_list, blizz_ah)
    db_functions.execute_values(blizz_ah_clean, 'blizz_ah_data')

    return

schedule.every().hour.do(recurring_task)
while True:
    schedule.run_pending()
