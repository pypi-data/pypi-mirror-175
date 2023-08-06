from pathlib import Path

import requests

from src.giteasy.github_releases import get_filename_fr_github_resp
from src.giteasy.github_releases import (
    get_tar_url_of_latest_release_of_a_public_github_repo ,
    download_latest_release_tarball_of_a_public_github_repo ,
    download_latest_release_of_public_github_repo ,
    )


##
rp = 'https://github.com/imahdimir/make-day-plan-in-Todoist-fr-notion'

##
url = get_tar_url_of_latest_release_of_a_public_github_repo(rp)
url

##
fp = download_latest_release_tarball_of_a_public_github_repo(rp)
fp

##
fp = download_latest_release_of_public_github_repo(rp)

##
import subprocess


##
subprocess.run(['cd' , str(fp)])

##
subprocess.run(['ls'])

##
