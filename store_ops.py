#!/usr/bin/env python3

import argparse
import datetime
import functools
import json
import logging
import os
import requests
import sys

import surl



logging.basicConfig(format='\033[3;1m%(message)s\033[0m')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def cached(path):
    snaps_cache = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            snaps_cache = {'snaps': []}
            try:
                logger.info('Loading cache ({})...'.format(path))
                with open(path) as fd:
                    snaps_cache = json.load(fd)
            except:
                logger.warning('Missing/Cold cache ...')
            try:
                return func(snaps_cache, *args, **kwargs)
            finally:
                logger.info('Saving cache ({})...'.format(path))
                with open(path, 'w') as fd:
                    payload = json.dumps(snaps_cache, indent=2, sort_keys=True)
                    fd.write(payload)
        return wrapper
    return decorator


def _make_partition(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i+size]


def get_search_results(config):
    headers = surl.DEFAULT_HEADERS.copy()
    headers['Authorization'] = surl.get_authorization_header(
        config.root, config.discharge)

    snaps = []
    url = '{}/api/v1/snaps/search?size=500&fields=snap_id,media'.format(
        surl.CONSTANTS[config.store_env]['api_base_url'])
    while url is not None:
        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        payload = r.json()

        snaps.extend(payload['_embedded']['clickindex:package'])

        # XXX store is returning an 'http' (no 's').
        _next = payload['_links'].get('next')
        url = _next['href'] if _next is not None else None

    return snaps


def get_snap_metrics(filters, config):
    headers = surl.DEFAULT_HEADERS.copy()
    headers['Authorization'] = surl.get_authorization_header(
        config.root, config.discharge)

    url = '{}/dev/api/snaps/metrics'.format(
        surl.CONSTANTS[config.store_env]['sca_base_url'])
    payload = {"filters": filters}
    r = requests.post(url=url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()['metrics']


@cached('snaps.json')
def refresh_cache(snaps_cache, config):
    logger.info('Fetching snaps ...')

    snaps = get_search_results(config)

    logger.info('Got {} snaps'.format(len(snaps)))

    snap_map = {
        s['snap_id']: {
            'snap_name': s['package_name'],
            'snap_id': s['snap_id'],
            'media': s['media'],
        } for s in snaps
    }

    yesterday = datetime.datetime.utcnow().date() - datetime.timedelta(1)
    start = end = yesterday.isoformat()
    for partition in _make_partition(list(snap_map.keys()), 400):
        logger.info('Fetching metrics for {} snaps ...'.format(len(partition)))

        filters = [{
            'metric_name': 'weekly_installed_base_by_channel',
            'snap_id': snap_id, "start": start, "end": end
        } for snap_id in partition]

        metrics = get_snap_metrics(filters, config)

        for m in metrics:
            snap_map[m['snap_id']].update({
                'installed_base': sum([sum(ch['values']) for ch in m['series']]),
                'updated_at': end
            })

    # Update cache. Eeew
    snaps_cache['snaps'] = list(snap_map.values())


def main():
    parser = argparse.ArgumentParser(
        description='Snap store status ...'
    )

    # Re-use surl credentials :-/
    auth_dir = os.path.abspath(os.path.expanduser('~/snap/surl/common'))
    if not os.path.exists(auth_dir):
        logger.warning(
            'Could not find `surl`, credentials will be stored in the local '
            'path. `snap install surl` to manage them in a single location.')
        auth_dir = os.path.abspath('.')

    try:
        config, remainder = surl.get_config_from_cli(parser, auth_dir)
    except surl.CliError as e:
        print(e)
        return 1
    except surl.CliDone:
        return 0

    parser.add_argument('-v', '--debug', action='store_true',
                        help='Prints request and response headers')

    args = parser.parse_args(remainder)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    refresh_cache(config)


if __name__ == '__main__':
    sys.exit(main())
