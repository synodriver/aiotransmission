"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
from typing import Optional, Union
from urllib.parse import urlparse, urlunparse

import aiohttp

from typing import List, NoReturn
from typing_extensions import Literal

from aiotr.typing import Request, Response, TagFactory
from aiotr.utils import DEFAULT_JSON_DECODER, DEFAULT_JSON_ENCODER, DEFAULT_HOST, DEFAULT_TIMEOUT, TagGen
from aiotr.exception import TransmissionException, TransmissionConnectException


class _BaseTransmissionClient:

    def __init__(self,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 url: Optional[str] = DEFAULT_HOST,
                 tag: Optional[TagFactory] = None
                 ):
        self.username = username
        self.password = password
        auth = f"{username}{password}@" if (username or password) else ""
        parsed = urlparse(url)

        self.url: str = urlunparse(parsed) if not auth else urlunparse(
            (parsed.scheme, auth + parsed.netloc, parsed.path, parsed.params, parsed.query,  # type: ignore
             parsed.fragment))  # type: ignore
        self.tag = tag if tag is not None else TagGen()

    # 3. Torrent Requests
    # 3.1 Torrent Action Requests
    async def torrent_start(self, ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        """
        "ids", which specifies which torrents to use.
                  All torrents are used if the "ids" argument is omitted.
                  "ids" should be one of the following:

        :param ids:
                  (1) an integer referring to a torrent id
                  (2) a list of torrent id numbers, sha1 hash strings, or both
                  (3) a string, "recently-active", for recently-active torrents
        :return: Response arguments: none
        """
        arguments = {"ids": ids} if ids else {}
        return await self.rpc("torrent-start", arguments)

    async def torrent_start_now(self,
                                ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        arguments = {"ids": ids} if ids else {}
        return await self.rpc("torrent-start-now", arguments)

    async def torrent_stop(self, ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        arguments = {"ids": ids} if ids else {}
        return await self.rpc("torrent-stop", arguments)

    async def torrent_verify(self, ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        arguments = {"ids": ids} if ids else {}
        return await self.rpc("torrent-verify", arguments)

    async def torrent_reannounce(self,
                                 ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        arguments = {"ids": ids} if ids else {}
        return await self.rpc("torrent-reannounce", arguments)

    # 3.2 Torrent Mutators
    async def torrent_set(self, bandwidthPriority: Optional[int] = None,
                          downloadLimit: Optional[int] = None,
                          downloadLimited: Optional[bool] = None,
                          files_wanted: Optional[List[str]] = None,
                          files_unwanted: Optional[List[str]] = None,
                          honorsSessionLimits: Optional[bool] = None,
                          ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None,
                          labels: Optional[List[str]] = None,
                          location: Optional[str] = None,
                          peer_limit: Optional[int] = None,
                          priority_high: Optional[List[str]] = None,
                          priority_low: Optional[List[str]] = None,
                          priority_normal: Optional[List[str]] = None,
                          queuePosition: Optional[int] = None,
                          seedIdleLimit: Optional[int] = None,
                          seedIdleMode: Optional[int] = None,
                          seedRatioLimit: Optional[float] = None,
                          seedRatioMode: Optional[int] = None,
                          trackerAdd: Optional[List[str]] = None,
                          trackerRemove: Optional[List[str]] = None,
                          trackerReplace: Optional[List[str]] = None,
                          uploadLimit: Optional[int] = None,
                          uploadLimited: Optional[bool] = None
                          ):
        """
            Just as an empty "ids" value is shorthand for "all ids", using an empty array
       for "files-wanted", "files-unwanted", "priority-high", "priority-low", or
       "priority-normal" is shorthand for saying "all files".

        :param bandwidthPriority:             this torrent's bandwidth tr_priority_t
        :param downloadLimit:                 maximum download speed (KBps)
        :param downloadLimited:               true if "downloadLimit" is honored
        :param files_wanted:                  indices of file(s) to download
        :param files_unwanted:                indices of file(s) to not download
        :param honorsSessionLimits:           true if session upload limits are honored
        :param ids:                           torrent list, as described in 3.1
        :param labels:                        array of string labels
        :param location:                      new location of the torrent's content
        :param peer_limit:                    maximum number of peers
        :param priority_high:                 indices of high-priority file(s)
        :param priority_low:                  indices of low-priority file(s)
        :param priority_normal:               indices of normal-priority file(s)
        :param queuePosition:                 position of this torrent in its queue [0...n)
        :param seedIdleLimit:                 torrent-level number of minutes of seeding inactivity
        :param seedIdleMode:                  which seeding inactivity to use.  See tr_idlelimit
        :param seedRatioLimit:                torrent-level seeding ratio
        :param seedRatioMode:                 which ratio to use.  See tr_ratiolimit
        :param trackerAdd:                    strings of announce URLs to add
        :param trackerRemove:                 ids of trackers to remove
        :param trackerReplace:                pairs of <trackerId/new announce URLs>
        :param uploadLimit:                   maximum upload speed (KBps)
        :param uploadLimited:                 true if "uploadLimit" is honored
        :return: Response arguments: none
        """
        arguments = {
            "bandwidthPriority": bandwidthPriority,
            "downloadLimit": downloadLimit,
            "downloadLimited": downloadLimited,
            "files-wanted": files_wanted,
            "files-unwanted": files_unwanted,
            "honorsSessionLimits": honorsSessionLimits,
            "ids": ids,
            "labels": labels,
            "location": location,
            "peer-limit": peer_limit,
            "priority-high": priority_high,
            "priority-low": priority_low,
            "priority-normal": priority_normal,
            "queuePosition": queuePosition,
            "seedIdleLimit": seedIdleLimit,
            "seedIdleMode": seedIdleMode,
            "seedRatioLimit": seedRatioLimit,
            "seedRatioMode": seedRatioMode,
            "trackerAdd": trackerAdd,
            "trackerRemove": trackerRemove,
            "trackerReplace": trackerReplace,
            "uploadLimit": uploadLimit,
            "uploadLimited": uploadLimited
        }
        return await self.rpc("torrent-set", arguments)

    # 3.5 Torrent Accessors
    async def torrent_get(self, fields: List[str],
                          format: Optional[str] = None,
                          ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        """

        :param fields:A required "fields" array of keys. (see list below)
        :param format: An optional "format" string specifying how to format the
       "torrents" response field. Allowed values are "objects" (default)
       and "table". (see "Response arguments" below)
        :param ids:An optional "ids" array as described in 3.1.
        :return:
        Response arguments:

           (1) A "torrents" array.

               If the "format" request was "objects" (default), "torrents" will
               be an array of objects, each of which contains the key/value
               pairs matching the request's "fields" arg. This was the only
               format before Transmission 3 and has some obvious programmer
               conveniences, such as parsing directly into Javascript objects.

               If the format was "table", then "torrents" will be an array of
               arrays. The first row holds the keys and each remaining row holds
               a torrent's values for those keys. This format is more efficient
               in terms of JSON generation and JSON parsing.

           (2) If the request's "ids" field was "recently-active",
               a "removed" array of torrent-id numbers of recently-removed
               torrents.

           Note: For more information on what these fields mean, see the comments
           in libtransmission/transmission.h.  The "source" column here
           corresponds to the data structure there.



         key                         | type                        | source
       ----------------------------+-----------------------------+---------
       activityDate                | number                      | tr_stat
       addedDate                   | number                      | tr_stat
       bandwidthPriority           | number                      | tr_priority_t
       comment                     | string                      | tr_info
       corruptEver                 | number                      | tr_stat
       creator                     | string                      | tr_info
       dateCreated                 | number                      | tr_info
       desiredAvailable            | number                      | tr_stat
       doneDate                    | number                      | tr_stat
       downloadDir                 | string                      | tr_torrent
       downloadedEver              | number                      | tr_stat
       downloadLimit               | number                      | tr_torrent
       downloadLimited             | boolean                     | tr_torrent
       editDate                    | number                      | tr_stat
       error                       | number                      | tr_stat
       errorString                 | string                      | tr_stat
       eta                         | number                      | tr_stat
       etaIdle                     | number                      | tr_stat
       file-count                  | number                      | tr_info
       files                       | array (see below)           | n/a
       fileStats                   | array (see below)           | n/a
       hashString                  | string                      | tr_info
       haveUnchecked               | number                      | tr_stat
       haveValid                   | number                      | tr_stat
       honorsSessionLimits         | boolean                     | tr_torrent
       id                          | number                      | tr_torrent
       isFinished                  | boolean                     | tr_stat
       isPrivate                   | boolean                     | tr_torrent
       isStalled                   | boolean                     | tr_stat
       labels                      | array (see below)           | tr_torrent
       leftUntilDone               | number                      | tr_stat
       magnetLink                  | string                      | n/a
       manualAnnounceTime          | number                      | tr_stat
       maxConnectedPeers           | number                      | tr_torrent
       metadataPercentComplete     | double                      | tr_stat
       name                        | string                      | tr_info
       peer-limit                  | number                      | tr_torrent
       peers                       | array (see below)           | n/a
       peersConnected              | number                      | tr_stat
       peersFrom                   | object (see below)          | n/a
       peersGettingFromUs          | number                      | tr_stat
       peersSendingToUs            | number                      | tr_stat
       percentDone                 | double                      | tr_stat
       pieces                      | string (see below)          | tr_torrent
       pieceCount                  | number                      | tr_info
       pieceSize                   | number                      | tr_info
       priorities                  | array (see below)           | n/a
       primary-mime-type           | string                      | tr_torrent
       queuePosition               | number                      | tr_stat
       rateDownload (B/s)          | number                      | tr_stat
       rateUpload (B/s)            | number                      | tr_stat
       recheckProgress             | double                      | tr_stat
       secondsDownloading          | number                      | tr_stat
       secondsSeeding              | number                      | tr_stat
       seedIdleLimit               | number                      | tr_torrent
       seedIdleMode                | number                      | tr_inactvelimit
       seedRatioLimit              | double                      | tr_torrent
       seedRatioMode               | number                      | tr_ratiolimit
       sizeWhenDone                | number                      | tr_stat
       startDate                   | number                      | tr_stat
       status                      | number                      | tr_stat
       trackers                    | array (see below)           | n/a
       trackerStats                | array (see below)           | n/a
       totalSize                   | number                      | tr_info
       torrentFile                 | string                      | tr_info
       uploadedEver                | number                      | tr_stat
       uploadLimit                 | number                      | tr_torrent
       uploadLimited               | boolean                     | tr_torrent
       uploadRatio                 | double                      | tr_stat
       wanted                      | array (see below)           | n/a
       webseeds                    | array (see below)           | n/a
       webseedsSendingToUs         | number                      | tr_stat
                                   |                             |
                                   |                             |
       -------------------+--------+-----------------------------+
       files              | array of objects, each containing:   |
                          +-------------------------+------------+
                          | bytesCompleted          | number     | tr_torrent
                          | length                  | number     | tr_info
                          | name                    | string     | tr_info
       -------------------+--------------------------------------+
       fileStats          | a file's non-constant properties.    |
                          | array of tr_info.filecount objects,  |
                          | each containing:                     |
                          +-------------------------+------------+
                          | bytesCompleted          | number     | tr_torrent
                          | wanted                  | boolean    | tr_info
                          | priority                | number     | tr_info
       -------------------+--------------------------------------+
       labels             | an array of strings:                 |
                          +-------------------------+------------+
                          | label                   | string     | tr_torrent
       -------------------+--------------------------------------+
       peers              | array of objects, each containing:   |
                          +-------------------------+------------+
                          | address                 | string     | tr_peer_stat
                          | clientName              | string     | tr_peer_stat
                          | clientIsChoked          | boolean    | tr_peer_stat
                          | clientIsInterested      | boolean    | tr_peer_stat
                          | flagStr                 | string     | tr_peer_stat
                          | isDownloadingFrom       | boolean    | tr_peer_stat
                          | isEncrypted             | boolean    | tr_peer_stat
                          | isIncoming              | boolean    | tr_peer_stat
                          | isUploadingTo           | boolean    | tr_peer_stat
                          | isUTP                   | boolean    | tr_peer_stat
                          | peerIsChoked            | boolean    | tr_peer_stat
                          | peerIsInterested        | boolean    | tr_peer_stat
                          | port                    | number     | tr_peer_stat
                          | progress                | double     | tr_peer_stat
                          | rateToClient (B/s)      | number     | tr_peer_stat
                          | rateToPeer (B/s)        | number     | tr_peer_stat
       -------------------+--------------------------------------+
       peersFrom          | an object containing:                |
                          +-------------------------+------------+
                          | fromCache               | number     | tr_stat
                          | fromDht                 | number     | tr_stat
                          | fromIncoming            | number     | tr_stat
                          | fromLpd                 | number     | tr_stat
                          | fromLtep                | number     | tr_stat
                          | fromPex                 | number     | tr_stat
                          | fromTracker             | number     | tr_stat
       -------------------+--------------------------------------+
       pieces             | A bitfield holding pieceCount flags  | tr_torrent
                          | which are set to 'true' if we have   |
                          | the piece matching that position.    |
                          | JSON doesn't allow raw binary data,  |
                          | so this is a base64-encoded string.  |
       -------------------+--------------------------------------+
       priorities         | an array of tr_info.filecount        | tr_info
                          | numbers. each is the tr_priority_t   |
                          | mode for the corresponding file.     |
       -------------------+--------------------------------------+
       trackers           | array of objects, each containing:   |
                          +-------------------------+------------+
                          | announce                | string     | tr_tracker_info
                          | id                      | number     | tr_tracker_info
                          | scrape                  | string     | tr_tracker_info
                          | tier                    | number     | tr_tracker_info
       -------------------+--------------------------------------+
       trackerStats       | array of objects, each containing:   |
                          +-------------------------+------------+
                          | announce                | string     | tr_tracker_stat
                          | announceState           | number     | tr_tracker_stat
                          | downloadCount           | number     | tr_tracker_stat
                          | hasAnnounced            | boolean    | tr_tracker_stat
                          | hasScraped              | boolean    | tr_tracker_stat
                          | host                    | string     | tr_tracker_stat
                          | id                      | number     | tr_tracker_stat
                          | isBackup                | boolean    | tr_tracker_stat
                          | lastAnnouncePeerCount   | number     | tr_tracker_stat
                          | lastAnnounceResult      | string     | tr_tracker_stat
                          | lastAnnounceStartTime   | number     | tr_tracker_stat
                          | lastAnnounceSucceeded   | boolean    | tr_tracker_stat
                          | lastAnnounceTime        | number     | tr_tracker_stat
                          | lastAnnounceTimedOut    | boolean    | tr_tracker_stat
                          | lastScrapeResult        | string     | tr_tracker_stat
                          | lastScrapeStartTime     | number     | tr_tracker_stat
                          | lastScrapeSucceeded     | boolean    | tr_tracker_stat
                          | lastScrapeTime          | number     | tr_tracker_stat
                          | lastScrapeTimedOut      | boolean    | tr_tracker_stat
                          | leecherCount            | number     | tr_tracker_stat
                          | nextAnnounceTime        | number     | tr_tracker_stat
                          | nextScrapeTime          | number     | tr_tracker_stat
                          | scrape                  | string     | tr_tracker_stat
                          | scrapeState             | number     | tr_tracker_stat
                          | seederCount             | number     | tr_tracker_stat
                          | tier                    | number     | tr_tracker_stat
       -------------------+-------------------------+------------+
       wanted             | an array of tr_info.fileCount        | tr_info
                          | 'booleans' true if the corresponding |
                          | file is to be downloaded.            |
       -------------------+--------------------------------------+
       webseeds           | an array of strings:                 |
                          +-------------------------+------------+
                          | webseed                 | string     | tr_info
                          +-------------------------+------------+



        """

        arguments = {"fields": fields, "format": format, "ids": ids}
        return await self.rpc("torrent-get", arguments)

    # 3.4 Adding a Torrent
    async def torrent_add(self, cookies: str,
                          download_dir: str,
                          filename: str,
                          metainfo: str,
                          paused: bool,
                          peer_limit: int,
                          bandwidthPriority: int,
                          files_wanted: List[str],
                          files_unwanted: List[str],
                          priority_high: List[str],
                          priority_low: List[str],
                          priority_normal: List[str]):
        """

        :param cookies:               pointer to a string of one or more cookies.
        :param download_dir:          path to download the torrent to
        :param filename:              filename or URL of the .torrent file
        :param metainfo:              base64-encoded .torrent content
        :param paused:                if true, don't start the torrent
        :param peer_limit:            maximum number of peers
        :param bandwidthPriority:     torrent's bandwidth tr_priority_t
        :param files_wanted:          indices of file(s) to download
        :param files_unwanted:        indices of file(s) to not download
        :param priority_high:         indices of high-priority file(s)
        :param priority_low:          indices of low-priority file(s)
        :param priority_normal:       indices of normal-priority file(s)
        :return:
        Response arguments: On success, a "torrent-added" object in the
                       form of one of 3.3's tr_info objects with the
                       fields for id, name, and hashString.

                       On failure due to a duplicate torrent existing,
                       a "torrent-duplicate" object in the same form.
        """
        arguments = {
            "cookies": cookies,
            "download-dir": download_dir,
            "filename": filename,
            "metainfo": metainfo,
            "paused": paused,
            "peer-limit": peer_limit,
            "bandwidthPriority": bandwidthPriority,
            "files-wanted": files_wanted,
            "files-unwanted": files_unwanted,
            "priority-high": priority_high,
            "priority-low": priority_low,
            "priority-normal": priority_normal,
        }
        return await self.rpc("torrent-add", arguments)

    # 3.5 Removing a Torrent
    async def torrent_remove(self, ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None,
                             delete_local_data: Optional[bool] = False):
        """

        :param ids: torrent list, as described in 3.1
        :param delete_local_data: delete local data. (default: false)
        :return:  Response arguments: none
        """
        arguments = {
            "ids": ids,
            "delete-local-data": delete_local_data
        }
        return await self.rpc("torrent-remove", arguments)

    # 3.6 Moving a Torrent
    async def torrent_set_location(self, location: str,
                                   ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None,
                                   move: Optional[bool] = False
                                   ):
        """

        :param location: the new torrent location
        :param ids: torrent list, as described in 3.1
        :param move: if true, move from previous location. otherwise, search "location" for files (default: false)
        :return:   Response arguments: none
        """
        arguments = {
            "ids": ids,
            "location": location,
            "move": move
        }
        return await self.rpc("torrent-set-location", arguments)

    #  3.7.  Renaming a Torrent's Path
    async def torrent_rename_path(self, path: str,
                                  name: str,
                                  ids: Optional[
                                      Union[int, List[Union[int, str]], Literal["recently-active"]]] = None, ):
        """
                 For more information on the use of this function, see the transmission.h
           documentation of tr_torrentRenamePath(). In particular, note that if this
           call succeeds you'll want to update the torrent's "files" and "name" field
           with torrent-get.
        :param path: the path to the file or folder that will be renamed
        :param name: the file or folder's new name
        :param ids:  the torrent torrent list, as described in 3.1 (must only be 1 torrent)
        :return:  Response arguments: "path", "name", and "id", holding the torrent ID integer
        """

        arguments = {
            "ids": ids,
            "name": name,
            "path": path
        }
        return await self.rpc("torrent-rename-path", arguments)

    # 4.  Session Requests
    # 4.1 Session Arguments
    # string                           | value type | description
    #    ---------------------------------+------------+-------------------------------------
    #    "alt-speed-down"                 | number     | max global download speed (KBps)
    #    "alt-speed-enabled"              | boolean    | true means use the alt speeds
    #    "alt-speed-time-begin"           | number     | when to turn on alt speeds (units: minutes after midnight)
    #    "alt-speed-time-enabled"         | boolean    | true means the scheduled on/off times are used
    #    "alt-speed-time-end"             | number     | when to turn off alt speeds (units: same)
    #    "alt-speed-time-day"             | number     | what day(s) to turn on alt speeds (look at tr_sched_day)
    #    "alt-speed-up"                   | number     | max global upload speed (KBps)
    #    "blocklist-url"                  | string     | location of the blocklist to use for "blocklist-update"
    #    "blocklist-enabled"              | boolean    | true means enabled
    #    "blocklist-size"                 | number     | number of rules in the blocklist
    #    "cache-size-mb"                  | number     | maximum size of the disk cache (MB)
    #    "config-dir"                     | string     | location of transmission's configuration directory
    #    "download-dir"                   | string     | default path to download torrents
    #    "download-queue-size"            | number     | max number of torrents to download at once (see download-queue-enabled)
    #    "download-queue-enabled"         | boolean    | if true, limit how many torrents can be downloaded at once
    #    "dht-enabled"                    | boolean    | true means allow dht in public torrents
    #    "encryption"                     | string     | "required", "preferred", "tolerated"
    #    "idle-seeding-limit"             | number     | torrents we're seeding will be stopped if they're idle for this long
    #    "idle-seeding-limit-enabled"     | boolean    | true if the seeding inactivity limit is honored by default
    #    "incomplete-dir"                 | string     | path for incomplete torrents, when enabled
    #    "incomplete-dir-enabled"         | boolean    | true means keep torrents in incomplete-dir until done
    #    "lpd-enabled"                    | boolean    | true means allow Local Peer Discovery in public torrents
    #    "peer-limit-global"              | number     | maximum global number of peers
    #    "peer-limit-per-torrent"         | number     | maximum global number of peers
    #    "pex-enabled"                    | boolean    | true means allow pex in public torrents
    #    "peer-port"                      | number     | port number
    #    "peer-port-random-on-start"      | boolean    | true means pick a random peer port on launch
    #    "port-forwarding-enabled"        | boolean    | true means enabled
    #    "queue-stalled-enabled"          | boolean    | whether or not to consider idle torrents as stalled
    #    "queue-stalled-minutes"          | number     | torrents that are idle for N minuets aren't counted toward seed-queue-size or download-queue-size
    #    "rename-partial-files"           | boolean    | true means append ".part" to incomplete files
    #    "rpc-version"                    | number     | the current RPC API version
    #    "rpc-version-minimum"            | number     | the minimum RPC API version supported
    #    "script-torrent-done-filename"   | string     | filename of the script to run
    #    "script-torrent-done-enabled"    | boolean    | whether or not to call the "done" script
    #    "seedRatioLimit"                 | double     | the default seed ratio for torrents to use
    #    "seedRatioLimited"               | boolean    | true if seedRatioLimit is honored by default
    #    "seed-queue-size"                | number     | max number of torrents to uploaded at once (see seed-queue-enabled)
    #    "seed-queue-enabled"             | boolean    | if true, limit how many torrents can be uploaded at once
    #    "speed-limit-down"               | number     | max global download speed (KBps)
    #    "speed-limit-down-enabled"       | boolean    | true means enabled
    #    "speed-limit-up"                 | number     | max global upload speed (KBps)
    #    "speed-limit-up-enabled"         | boolean    | true means enabled
    #    "start-added-torrents"           | boolean    | true means added torrents will be started right away
    #    "trash-original-torrent-files"   | boolean    | true means the .torrent file of added torrents will be deleted
    #    "units"                          | object     | see below
    #    "utp-enabled"                    | boolean    | true means allow utp
    #    "version"                        | string     | long version string "$version ($revision)"
    #    ---------------------------------+------------+-----------------------------+
    #    units                            | object containing:                       |
    #                                     +--------------+--------+------------------+
    #                                     | speed-units  | array  | 4 strings: KB/s, MB/s, GB/s, TB/s
    #                                     | speed-bytes  | number | number of bytes in a KB (1000 for kB; 1024 for KiB)
    #                                     | size-units   | array  | 4 strings: KB/s, MB/s, GB/s, TB/s
    #                                     | size-bytes   | number | number of bytes in a KB (1000 for kB; 1024 for KiB)
    #                                     | memory-units | array  | 4 strings: KB/s, MB/s, GB/s, TB/s
    #                                     | memory-bytes | number | number of bytes in a KB (1000 for kB; 1024 for KiB)
    #                                     +--------------+--------+------------------+
    #
    #    "rpc-version" indicates the RPC interface version supported by the RPC server.
    #    It is incremented when a new version of Transmission changes the RPC interface.
    #
    #    "rpc-version-minimum" indicates the oldest API supported by the RPC server.
    #    It is changes when a new version of Transmission changes the RPC interface
    #    in a way that is not backwards compatible.  There are no plans for this
    #    to be common behavior.
    # 4.1.1.  Mutators
    async def session_set(self,
                          alt_speed_down: Optional[int] = None,
                          alt_speed_enabled: Optional[bool] = None,
                          alt_speed_time_begin: Optional[int] = None,
                          alt_speed_time_enabled: Optional[bool] = None,
                          alt_speed_time_end: Optional[int] = None,
                          alt_speed_time_day: Optional[int] = None,
                          alt_speed_up: Optional[int] = None,
                          blocklist_url: Optional[str] = None,
                          blocklist_enabled: Optional[bool] = None,
                          cache_size_mb: Optional[int] = None,
                          download_dir: Optional[str] = None,
                          download_queue_size: Optional[int] = None,
                          download_queue_enabled: Optional[bool] = None,
                          dht_enabled: Optional[bool] = None,
                          encryption: Optional[str] = None,
                          idle_seeding_limit: Optional[int] = None,
                          idle_seeding_limit_enabled: Optional[bool] = None,
                          incomplete_dir: Optional[str] = None,
                          incomplete_dir_enabled: Optional[bool] = None,
                          lpd_enabled: Optional[bool] = None,
                          peer_limit_global: Optional[int] = None,
                          peer_limit_per_torrent: Optional[int] = None,
                          pex_enabled: Optional[bool] = None,
                          peer_port: Optional[int] = None,
                          peer_port_random_on_start: Optional[bool] = None,
                          port_forwarding_enabled: Optional[bool] = None,
                          queue_stalled_enabled: Optional[bool] = None,
                          queue_stalled_minutes: Optional[int] = None,
                          rename_partial_files: Optional[bool] = None,
                          script_torrent_done_filename: Optional[str] = None,
                          script_torrent_done_enabled: Optional[bool] = None,
                          seedRatioLimit: Optional[float] = None,
                          seedRatioLimited: Optional[bool] = None,
                          seed_queue_size: Optional[int] = None,
                          seed_queue_enabled: Optional[bool] = None,
                          speed_limit_down: Optional[int] = None,
                          speed_limit_down_enabled: Optional[bool] = None,
                          speed_limit_up: Optional[int] = None,
                          speed_limit_up_enabled: Optional[bool] = None,
                          start_added_torrents: Optional[bool] = None,
                          trash_original_torrent_files: Optional[bool] = None,
                          units: Optional[dict] = None,
                          utp_enabled: Optional[bool] = None,
                          ):
        """

        :param alt_speed_down:
        :param alt_speed_enabled:
        :param alt_speed_time_begin:
        :param alt_speed_time_enabled:
        :param alt_speed_time_end:
        :param alt_speed_time_day:
        :param alt_speed_up:
        :param blocklist_url:
        :param blocklist_enabled:
        :param cache_size_mb:
        :param download_dir:
        :param download_queue_size:
        :param download_queue_enabled:
        :param dht_enabled:
        :param encryption:
        :param idle_seeding_limit:
        :param idle_seeding_limit_enabled:
        :param incomplete_dir:
        :param incomplete_dir_enabled:
        :param lpd_enabled:
        :param peer_limit_global:
        :param peer_limit_per_torrent:
        :param pex_enabled:
        :param peer_port:
        :param peer_port_random_on_start:
        :param port_forwarding_enabled:
        :param queue_stalled_enabled:
        :param queue_stalled_minutes:
        :param rename_partial_files:
        :param script_torrent_done_filename:
        :param script_torrent_done_enabled:
        :param seedRatioLimit:
        :param seedRatioLimited:
        :param seed_queue_size:
        :param seed_queue_enabled:
        :param speed_limit_down:
        :param speed_limit_down_enabled:
        :param speed_limit_up:
        :param speed_limit_up_enabled:
        :param start_added_torrents:
        :param trash_original_torrent_files:
        :param units:
        :param utp_enabled:
        :return: Response arguments: none
        """
        arguments = {
            "alt-speed-down": alt_speed_down,
            "alt-speed-enabled": alt_speed_enabled,
            "alt-speed-time-begin": alt_speed_time_begin,
            "alt-speed-time-enabled": alt_speed_time_enabled,
            "alt-speed-time-end": alt_speed_time_end,
            "alt-speed-time-day": alt_speed_time_day,
            "alt-speed-up": alt_speed_up,
            "blocklist-url": blocklist_url,
            "blocklist-enabled": blocklist_enabled,
            "cache-size-mb": cache_size_mb,
            "download-dir": download_dir,
            "download-queue-size": download_queue_size,
            "download-queue-enabled": download_queue_enabled,
            "dht-enabled": dht_enabled,
            "encryption": encryption,
            "idle-seeding-limit": idle_seeding_limit,
            "idle-seeding-limit-enabled": idle_seeding_limit_enabled,
            "incomplete-dir": incomplete_dir,
            "incomplete-dir-enabled": incomplete_dir_enabled,
            "lpd-enabled": lpd_enabled,
            "peer-limit-global": peer_limit_global,
            "peer-limit-per-torrent": peer_limit_per_torrent,
            "pex-enabled": pex_enabled,
            "peer-port": peer_port,
            "peer-port-random-on-start": peer_port_random_on_start,
            "port-forwarding-enabled": port_forwarding_enabled,
            "queue-stalled-enabled": queue_stalled_enabled,
            "queue-stalled-minutes": queue_stalled_minutes,
            "rename-partial-files": rename_partial_files,
            "script-torrent-done-filename": script_torrent_done_filename,
            "script-torrent-done-enabled": script_torrent_done_enabled,
            "seedRatioLimit": seedRatioLimit,
            "seedRatioLimited": seedRatioLimited,
            "seed-queue-size": seed_queue_size,
            "seed-queue-enabled": seed_queue_enabled,
            "speed-limit-down": speed_limit_down,
            "speed-limit-down-enabled": speed_limit_down_enabled,
            "speed-limit-up": speed_limit_up,
            "speed-limit-up-enabled": speed_limit_up_enabled,
            "start-added-torrents": start_added_torrents,
            "trash-original-torrent-files": trash_original_torrent_files,
            "units": units,
            "utp-enabled": utp_enabled,
        }
        return await self.rpc("session-set", arguments)

    # 4.1.2.  Accessors
    async def session_get(self, fields: Optional[List[str]] = None):
        """

        :param fields: an optional "fields" array of keys (see 4.1)
        :return: Response arguments: key/value pairs matching the request's "fields"
       argument if present, or all supported fields (see 4.1) otherwise.
        """
        arguments = {
            "fields": fields
        }
        return await self.rpc("session-get", arguments)

    # 4.2.  Session Statistics
    async def session_stats(self):
        """

        :return:
        Response arguments:

           string                     | value type
           ---------------------------+-------------------------------------------------
           "activeTorrentCount"       | number
           "downloadSpeed"            | number
           "pausedTorrentCount"       | number
           "torrentCount"             | number
           "uploadSpeed"              | number
           ---------------------------+-------------------------------+
           "cumulative-stats"         | object, containing:           |
                                      +------------------+------------+
                                      | uploadedBytes    | number     | tr_session_stats
                                      | downloadedBytes  | number     | tr_session_stats
                                      | filesAdded       | number     | tr_session_stats
                                      | sessionCount     | number     | tr_session_stats
                                      | secondsActive    | number     | tr_session_stats
           ---------------------------+-------------------------------+
           "current-stats"            | object, containing:           |
                                      +------------------+------------+
                                      | uploadedBytes    | number     | tr_session_stats
                                      | downloadedBytes  | number     | tr_session_stats
                                      | filesAdded       | number     | tr_session_stats
                                      | sessionCount     | number     | tr_session_stats
                                      | secondsActive    | number     | tr_session_stats
        """
        arguments = {}
        return await self.rpc("session-stats", arguments)

    # 4.3.  Blocklist
    async def blocklist_update(self):
        """

        :return:  Response arguments: a number "blocklist-size"
        """
        arguments = {}
        return await self.rpc("blocklist-update", arguments)

    # 4.4.  Port Checking
    async def port_test(self):
        """
            This method tests to see if your incoming peer port is accessible
         from the outside world.
        :return: Response arguments: a bool, "port-is-open"
        """
        arguments = {}
        return await self.rpc("port-test", arguments)

    # 4.5.  Session shutdown
    async def session_close(self):
        """
         This method tells the transmission session to shut down.
        :return:  Response arguments: none
        """
        arguments = {}
        return await self.rpc("session-close", arguments)

    # 4.6.  Queue Movement Requests
    async def queue_move_top(self, ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        """
        :param ids:  array   torrent list, as described in 3.1.
        :return:  Response arguments: none

        """
        arguments = {"ids": ids}
        return await self.rpc("queue-move-top", arguments)

    async def queue_move_up(self, ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        arguments = {"ids": ids}
        return await self.rpc("queue-move-up", arguments)

    async def queue_move_down(self,
                              ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        arguments = {"ids": ids}
        return await self.rpc("queue-move-down", arguments)

    async def queue_move_bottom(self,
                                ids: Optional[Union[int, List[Union[int, str]], Literal["recently-active"]]] = None):
        arguments = {"ids": ids}
        return await self.rpc("queue-move-bottom", arguments)

    # 4.7.  Free Space
    async def free_space(self, path: str):
        """

        :param path: string  the directory to query
        :return: Response arguments:

   string      | value type & description
   ------------+----------------------------------------------------------
   "path"      | string  same as the Request argument
   "size-bytes"| number  the size, in bytes, of the free space in that directory

        """
        arguments = {"path": path}
        return await self.rpc("free-space", arguments)

    # 5.0.  Protocol Versions

    async def rpc(self, method: str, arguments: dict):
        arguments = {k: v for k, v in arguments.items() if v}
        request = Request(
            method=method,
            arguments=arguments,
            tag=self.tag())  # type: ignore

        return await self.send_request(request)

    async def send_request(self, request: Request):
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class TransmissionClient(_BaseTransmissionClient):
    def __init__(self, username: Optional[str] = None,
                 password: Optional[str] = None,
                 url: Optional[str] = DEFAULT_HOST,
                 tag: Optional[TagFactory] = None,
                 timeout: Union[int, float] = DEFAULT_TIMEOUT,
                 **kwargs):
        super().__init__(username, password, url, tag)
        self.timeout = timeout
        self.headers = {"X-Transmission-Session-Id": "", "Host": ""}  # todo need update and verify
        self.client_session = aiohttp.ClientSession()

        self.kwargs = kwargs  # 用于session.post
        self.loads = self.kwargs.pop("loads") if "loads" in self.kwargs else DEFAULT_JSON_DECODER  # json serialize
        self.dumps = self.kwargs.pop("dumps") if "dumps" in self.kwargs else DEFAULT_JSON_ENCODER

    @property
    def host(self):
        return self.headers.get("Host")

    @host.setter  # type: ignore
    def set_host(self, host: str):
        self.headers.update(Host=host)

    @property
    def session_id(self):
        return self.headers.get("X-Transmission-Session-Id")

    @session_id.setter  # type: ignore
    def set_session_id(self, session_id: str):
        self.headers.update({"X-Transmission-Session-Id": session_id})

    async def send_request(self, request: Request) -> Union[dict, NoReturn, None]:
        """

        :param request:
        :return:
        """
        while True:
            try:
                async with self.client_session.post(self.url,
                                                    json=request,
                                                    headers=self.headers,
                                                    timeout=self.timeout,
                                                    **self.kwargs) as resp:
                    if resp.status == 409:
                        self.session_id = resp.headers["X-Transmission-Session-Id"]  # type: ignore
                        continue
                    try:
                        data: Response = await resp.json(loads=self.loads)
                        if data["tag"] != request["tag"]:
                            raise TransmissionException('unexpected tag: {}'.format(data["tag"]))
                        if data["result"] != "success":
                            raise TransmissionException('unexpected result: {}'.format(data))
                        return data["arguments"]
                    # 没有result就是异常
                    except KeyError:
                        raise TransmissionException('unexpected result: {}'.format(data))
            except aiohttp.ClientConnectionError as err:
                raise TransmissionConnectException(str(err)) from err

    async def close(self) -> None:
        await self.client_session.close()  # type: ignore
