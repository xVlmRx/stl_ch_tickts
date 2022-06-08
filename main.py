import requests
import json
from prettytable import PrettyTable

api_key = "API_key"
url = 'https://api.selectel.ru/support/tickets'
headers = {'X-Token': api_key,
           'Content-Type': 'application/json'}
query_params = {"only_opened": "True", "page": "1"}
table_ticket_id = PrettyTable()
table_ticket_subject = PrettyTable()
table_ticket_comments = PrettyTable()
table_comments = PrettyTable()
tickets_list = []
comments_list = []


def get_from_api(ticket_id_get="no_tickets_id"):
    try:
        if ticket_id_get == "no_tickets_id":
            response = requests.get(url, headers=headers, params=query_params)
        else:
            response = requests.get('{}/{}/comments'.format(url, ticket_id_get), headers=headers)
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Failed to call http api '{}', error is '{}'".format(url, e))
    try:
        data = response.json()
    except ValueError as e:
        raise RuntimeError("Selectel endpoint '{}' seems down, decoding error is ".format(url), e)
    return data


def ticket_comments(ticket_id="no_tickets_id"):
    for comments in get_from_api(ticket_id).get('items', "Can't find key in dictionary"):
        if comments.get('is_client_author') is False and comments.get('is_client_read') is False:
            comments_list.append(comments.get('body'))
    return comments_list


if __name__ == '__main__':
    for tickets in get_from_api().get('items', "Can't find key in dictionary"):
        if tickets.get('is_client_author') is False and tickets.get('is_client_read') == False:
            # table_comments.field_names = ["Field name", "Data"]
            # table_comments.add_row(["ID тикета:", tickets.get('number')])
            # table_comments.add_row(["Тема тикета:", tickets.get('summary')])
            # table_comments.add_row(["Комментарии к тикету:", '\n'.join(ticket_comments(str(tickets.get('number'))))])
            tickets_list.append("///Subject:{}///".format(tickets.get('summary')))
            tickets_list.append("URL: https://my.selectel.ru/tickets/conversation/{}".format(tickets.get('number')))
            tickets_list.append("---Comments:---\n{}".format('\n'.join(ticket_comments(str(tickets.get('number'))))))
            tickets_list.append("################################################################################")
            comments_list = []
    if len(tickets_list) != 0:
        print('\n'.join(tickets_list))
        # print(table_comments)
    else:
        print('All OK!!!')
