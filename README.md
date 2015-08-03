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
- What line did it happen on?
- What station did it happen at?
- Depending on the station, which lines would it effect?
- What direction was the train traveling?


Contact me on twitter, @jimmysthoughts for questions.
Feel free to submit a PR.