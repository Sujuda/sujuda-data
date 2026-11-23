# sujuda-data

The masjid list used by the **Sujuda** app (Mosques tab). The app downloads
`masjids.json` from this repository once a day, so changes reach users
**without an app update**. The app also ships with a copy built in, used when
the phone is offline or this file can't be read.

## Editing the list

1. Open `masjids.json` and tap the pencil (edit) icon.
2. Make your change, then **Commit changes**.
3. Check the result under **Actions**: a green tick means the list is fine.
   A red X means the app will ignore this version and keep the last good
   one; open the run to see which line is wrong.

Phones pick up the change within about a day (the next time the Mosques tab
opens after their daily check).

## Fields of one masjid

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Unique, lowercase with dashes, e.g. `masjid-al-jannah`. Don't change it later. |
| `name` | yes | Shown in the app. |
| `latitude`, `longitude` | yes | Position, as numbers. |
| `coordinatesApproximate` | no | `true` if the position is only roughly right; directions then use the address. |
| `address`, `city`, `country` | no | Shown under the name. |
| `website` | no | The masjid's website ("Website" button). |
| `prayerTimesUrl` | no | A page that is **only** the prayer-time table (often the widget their site embeds). Shown by the "Prayer times" button. |
| `prayerTimeSourceUrl` + `prayerTimesSelector` | no | Instead of `prayerTimesUrl`: the page with the table, and the CSS selector of the table on it. The app shows only that part. |
| `prayerTimesMustContain` | no | Text the table must contain (e.g. `Fajr`), to pick the right one. |
| `verified` | no | `true` for entries you've checked yourself. |
| `notes` | no | For you; not shown in the app. |

Without `prayerTimesUrl` or `prayerTimesSelector`, a masjid has no "Prayer
times" button.

Links must start with `https://` (or `http://`).

## Announcements and the minimum app version (`app.json`)

The app reads `app.json` twice a day. Edit it the same way as the masjid
list (pencil icon, **Commit changes**, then check **Actions** for the green
tick).

### Show a message on Home (for example, Eid Mubarak)

Add an entry to `"announcements"`:

```json
{
  "version": 1,
  "minBuild": 0,
  "announcements": [
    {
      "id": "eid-al-fitr-2027",
      "title": "Eid Mubarak",
      "message": "Taqabbal Allahu minna wa minkum. Wishing you and your family a blessed Eid.",
      "start": "2027-03-10",
      "end": "2027-03-12"
    }
  ]
}
```

| Field | Rules |
|---|---|
| `id` | Unique, lowercase letters, digits and dashes. Use a new one for each message. |
| `title` | Up to 60 characters. |
| `message` | Up to 300 characters, plain text (no `<` or `>`). |
| `start`, `end` | Dates like `2027-03-10`. Shown from `start` to `end` (inclusive), at most 14 days. |
| `link`, `linkLabel` | Optional. The link must start with `https://` and be on `sujuda.github.io` or `play.google.com`. `linkLabel` is the button text (up to 30 characters; default "Learn more"). |

People see it as a card at the top of Home the next time they open the
app, and can close it. Old entries can stay or be deleted.

### Ask everyone on an old version to update

Set `"minBuild"` to the version code of the new release (the number shown
next to the App Bundle in the build, e.g. `170`). Phones with an older
version, **and only when Google Play confirms the update is available**,
see Google Play's update screen, and a "Please update" card on Home if
they close it. The app is never locked and the update always comes from
Google Play, so a wrong number can't harm anyone. Use `0` to turn it off.

If anything in `app.json` breaks a rule, the check fails (red X) and the
app ignores the whole file, keeping its last good copy.
