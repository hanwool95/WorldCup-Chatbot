# World Cup information Chat Bot

Hanwool Kim(hanwool95@snu.ac.kr)

# How To


<b>installation</b><br>
<pre>
pip install -r requirement.txt
npm install
</pre>
<br>
<b>Crawling Data</b><br>

<pre>
python crawling/team.py
</pre>


<b>Training Data Set</b><br>
<pre>
python train/openqa.py
</pre>

<b>runserver</b>
<pre>
node chating_interface/Server.js
cd api
uvicorn api:app --reload
</pre>

chatbot
<a href="127.0.0.1:3737/">127.0.0.1:3737/</a>