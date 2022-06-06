import requests
import json
from prettytable import PrettyTable

api_key = "gBdBXfw2YirQ90kLy2kqtDhWF_20413"
url = 'https://api.selectel.ru/support/tickets'
headers = {'X-Token': api_key,
           'Content-Type': 'application/json'}
query_params = {"only_opened": "True", "page": "1"}
table_ticket_id = PrettyTable()
table_ticket_subject = PrettyTable()
table_ticket_comments = PrettyTable()
table_comments = PrettyTable()
tickets_list = []


def get_from_api(ticket_id_get="no_tickets_id"):
    if ticket_id_get == "no_tickets_id":
        return requests.get(url, headers=headers, params=query_params).json()
    else:
        return requests.get('{}/{}/comments'.format(url, ticket_id_get), headers=headers).json()


def ticket_comments(ticket_id="no_tickets_id"):
    for comments in get_from_api(ticket_id).get('items', "Can't find key in dictionary"):
        if comments.get('is_client_author') == False and comments.get('is_client_read') == True:
            return comments.get('body')


if __name__ == '__main__':
    for tickets in get_from_api().get('items', "Can't find key in dictionary"):
        if tickets.get('is_client_author') == False and tickets.get('is_client_read') == True:
            table_comments.field_names = ["Field name", "Data"]
            table_comments.add_row(["ID тикета:", tickets.get('number')])
            table_comments.add_row(["Тема тикета:", tickets.get('summary')])
            table_comments.add_row(["Комментарии к тикету:", ticket_comments(str(tickets.get('number')))])
            tickets_list.append("Subject:{}".format(tickets.get('summary')))
            tickets_list.append("https://my.selectel.ru/tickets/conversation/{}".format(tickets.get('number')))
    print('\n'.join(tickets_list))
    print(table_comments)