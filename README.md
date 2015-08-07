Metro Data Extractor
====================

This is a quick hack job to convert metro service reports into some form of structured data.  

The entire output is in JSON, which I've dumped in the test_data/ directory.
 
Some issues:
------------
- Sometimes two messages get combined by accident.
- Delays and Gaps are just whatever number happens to be in the message along with the word ('minute' and ('gap' or 'delay'))
- I didn't check the timestamp too heavily either.
- Python: My module/class/file/import structure is terrible.  Can you help me fix it?

Future Stuff:
-------------
- More accurate color/line reporting
- What station did it happen at?
- Depending on the station, which lines would it effect?
- What direction was the train traveling?


Sample Data
-----------
```json
[{
proc_text: "4:38 p.m. a shady grove-bound red line train at cleveland park was offloaded due to a door problem. passengers experienced a 10-minute delay.",
expressed: false,
id: "3292_16_38",
gap: null,
delay: {
minutes: 10
},
colors: [
"red"
],
event_dtg: "2015-08-06T16:38:00"
},
{
proc_text: "5:55 a.m. a largo town center-bound blue line train at king street did not operate, resulting in an 8-minute gap in service.",
expressed: false,
id: "3292_5_55",
gap: {
minutes: 8
},
delay: null,
colors: [
"blue"
],
event_dtg: "2015-08-06T05:55:00"
},
{
proc_text: "8:10 a.m. a branch avenue-bound green line train at suitland was expressed for schedule adherence/improved train spacing.",
expressed: true,
id: "3292_8_10",
gap: null,
delay: null,
colors: [
"green"
],
event_dtg: "2015-08-06T08:10:00"
}]
```

Contact me on twitter, [@jimmysthoughts](https://twitter.com/jimmysthoughts) for questions.
Feel free to submit a PR.
