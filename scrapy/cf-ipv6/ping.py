from pprint import pprint
from multiping import MultiPing


def multi_ping(ip_list):
    # Create a MultiPing object to test three hosts / addresses
    mp = MultiPing(ip_list)

    # Send the pings to those addresses
    mp.send()

    # With a 1 second timout, wait for responses (may return sooner if all
    # results are received).
    responses, no_responses = mp.receive(1)

    pprint(sorted(responses.items(), key=lambda obj: obj[1], reverse=True))


if __name__ == '__main__':
    ip_list = []
    f = open('cf_valid_ipv6.txt', 'r')
    item_list = f.readlines()
    for i in item_list:
        ip = i.split()[0]
        ip_list.append(ip)

    multi_ping(ip_list)
