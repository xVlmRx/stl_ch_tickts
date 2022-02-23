import requests
import json

url = 'https://api.selectel.ru/support/tickets'
headers = {'X-Token': '$API_key',
           'Content-Type': 'application/json'}
query_params = {"only_opened": "True", "page": "1"}


def get_from_api(ticket_id_get="no_tickets_id"):
    if ticket_id_get == "no_tickets_id":
        return requests.get(url, headers=headers, params=query_params).json()
    else:
        return requests.get(url + "/" + ticket_id_get + "/comments", headers=headers).json()


def ticket_comments(ticket_id="no_tickets_id"):
    for comments in get_from_api(ticket_id).get('items', "Can't find key in dictionary"):
        if comments.get('is_client_author') == False and comments.get('is_client_read') == True:
            return comments.get('body')


if __name__ == '__main__':
    for tickets in get_from_api().get('items', "Can't find key in dictionary"):
        if tickets.get('is_client_author') == False and tickets.get('is_client_read') == True:
            print("ID тикета:", tickets.get('number'), "\n", "Тема тикета:", tickets.get('summary'), "\n--- --- --- --- ---\nКомментарии к тикету:\n--- --- --- --- ---\n", ticket_comments(str(tickets.get('number'))))
            print("*** *** *** *** ***")