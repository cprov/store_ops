# store_ops

Snap Store Operations


```
$ virtualenv -p python3 env
...

$ . env/bin/activate
(env) $ ./setup.py develop
...


(env) $ ./env/bin/store_ops.py -s production -e celso.providelo@canonical.com -p package_access -p package_metrics
Password for celso.providelo@canonical.com: 🔑
Second-factor auth for production: 🔑
Loading cache (snaps.json)...
Fetching snaps ...
Got 1495 snaps
Fetching metrics for 400 snaps ...
Fetching metrics for 400 snaps ...
Fetching metrics for 400 snaps ...
Fetching metrics for 295 snaps ...
Saving cache (snaps.json)...

(env) $ jq '.snaps | map(select(.snap_name == "surl"))' snaps.json
[
  {
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

By default, if `surl` snap is installed, the user prexisting credentials can be reused:

```
./env/bin/store_ops.py -l
Available credendials:
  prod-store (production)
  prod-metrics (production)
...


$ ./env/bin/store_ops.py -a prod-metrics
Loading cache (snaps.json)...
Fetching snaps ...
...

```
