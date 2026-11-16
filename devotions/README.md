# Family Devotion data

The Devotion tab reads these files.

- `index.json` lists each quarter's booklet, with its file and its first and last dates. The app opens whichever quarter contains today, or the next one coming up.
- `common.json` holds everything the booklets share: the four prayer orders (Morning, Noon, Early Evening, Close of the Day), the Apostles' Creed, the Lord's Prayer, and the prayer topic for each day of the week.
- `winter-2026-27.json` is one quarter: each week's theme, introduction, catechism (tagged pre, 1st, 2nd, 3rd or all), six readings (Mon to Sat, with the Sunday School story marked), discussion questions, verse of the week and hymn.

To add a new booklet: add its file and one line in `index.json`. Week start dates must be Sundays.

## ESV API rules (api.esv.org)

The readings are fetched live from Crossway's ESV API. The app keeps to its terms:

- Noncommercial use only.
- One request per passage someone opens, never prefetched, each far below 500 verses or half a book.
- Throttled to 20 requests a minute, well under 60 a minute, 1,000 an hour and 5,000 a day.
- At most 8 passages are cached on a device, for at most two weeks, so local storage never nears 500 consecutive verses or half a book.
- Every ESV passage shows "(ESV)" and the full copyright notice is at the foot of every page that shows ESV text.
- ESV text is never fed into the main verse-by-verse reader.

If the ESV can't load (offline, Crossway down, or the key refused), the same passage shows from the app's own WEB text, or KJV where WEB is missing, with a note saying why. Each reading carries `ranges` ([book, startChapter, startVerse, endChapter, endVerse], with 999 meaning to the end of the chapter) for this fallback.

The booklet files are saved on the phone after the first load, so the tab opens offline.
