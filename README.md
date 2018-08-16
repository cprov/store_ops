# store_ops

Snap Store Operations


```
$ virtualenv -p python3 env
...

$ . env/bin/activate

(env) $ ./setup.py develop
...


(env) $ ./store_ops.py -s production -e celso.providelo@canonical.com -p package_access -p package_metrics snaps | jq '.snaps | map(select(.snap_name == "surl"))'
Password for celso.providelo@canonical.com: 🔑
Second-factor auth for production: 🔑
Fetching snaps ...
Got 1495 snaps
Fetching metrics ...
[
  {
    "developer_username": "cprov",
    "developer_validation": "unproven",
    "installed_base": 110,
    "media": [
      {
        "type": "icon",
        "url": "https://dashboard.snapcraft.io/site_media/appmedia/2018/08/surl.png"
      }
    ],
    "snap_id": "LpV8761EjlAPqeXxfYhQvpSWgpxvEWpN",
    "snap_name": "surl",
    "updated_at": "2018-08-15"
  }
]
```

By default, if `surl` snap is installed, the user's prexisting credentials will be reused:


```
./env/bin/store_ops.py -l
Available credendials:
  prod-store (production)
  prod-metrics (production)
...


./store_ops.py -a prod-metrics snaps |  jq '.snaps | map(select(.media | map(select(.type == "icon")) | length == 0)) | map(select(.developer_username != "canonical")) | sort_by(.installed_base) | reverse | .[:2]'
Fetching snaps ...
Got 1498 snaps
Fetching metrics ...
[
  {
    "snap_id": "SMmdWwqPVDscid2Ragxl3kLgGwfbTN5h",
    "media": [
      {
        "url": "https://dashboard.snapcraft.io/site_media/appmedia/2018/05/trackmania.png",
        "type": "screenshot"
      },
      ...
    ],
    "installed_base": <redacted>,
    "developer_validation": "unproven",
    "developer_username": "snapcrafters",
    "snap_name": "tmnationsforever"
  },
  {
    "snap_id": "JlrNGBIqwjdB64Hq94WTbELDWCjFwhta",
    "media": [
      {
        "url": "https://dashboard.snapcraft.io/site_media/appmedia/2016/06/rename.screenshot.png",
        "type": "screenshot"
      },
      ...
    ],
    "installed_base": <redacted>,
    "developer_validation": "unproven",
    "developer_username": "filebot",
    "snap_name": "filebot"
  }
]
```
