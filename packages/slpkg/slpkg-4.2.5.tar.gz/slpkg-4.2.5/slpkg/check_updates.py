#!/usr/bin/python3
# -*- coding: utf-8 -*-


import urllib3
from dataclasses import dataclass

from slpkg.configs import Configs


@dataclass
class CheckUpdates:
    sbo_repo_url: str = Configs.sbo_repo_url
    sbo_repo_path: str = Configs.sbo_repo_path
    chglog_txt: str = Configs.chglog_txt

    def updates(self):

        local_chg_txt = f'{self.sbo_repo_path}/{self.chglog_txt}'

        with open(local_chg_txt, 'r', encoding='utf-8') as f:
            local_date = f.readline().strip()

        http = urllib3.PoolManager()
        repo = http.request(
            'GET', f'{self.sbo_repo_url}/{self.chglog_txt}')

        repo_date = repo.data.decode().split('\\')[0][:len(local_date)]
        if repo_date > local_date:
            print('\nThere are new updates available.\n')
        else:
            print('\nNo updated packages since the last check.\n')
