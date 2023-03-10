# EVITA-Japanese-DialogueSystem
Japanese Dialogue System developed in EVITA project

<h2>Contents</h2>
<ol>
    <li> Credits</li>
    <li> How to</li>
    <li> References</li>
</ol>

<h2>1. Credits</h2>
This folder contains a Japanese dialogue system for the e-VITA Virtual Coach application, based on Rasa Open Source Conversational AI version 3.4: 
https://rasa.com/docs/

The system was developed in the EU-JP cooperation project e-VITA: https://www.e-vita.coach/ <br>
The work has been supported by the Strategic Information and Communications R&D Promotion Programme (SCOPE) of Ministry of Internal Affairs and Communications (MIC), Grant no. JPJ000595.
https://www.soumu.go.jp/english/

Files copyright AI Research Center (AIRC) at National Institute of Advanced Industrial Science and Technology (AIST), unless otherwise indicated or part of the Rasa framework. 
https://www.airc.aist.go.jp/en/
<br>
Licence: Apache 2.0.

Programmer: Tatsuya Kudo<br>
Project Leader at AIRC: Kristiina Jokinen

We thank all the project partners for discussions in the design of the system, checking translations, and participating in the Conversation Driven Development 
https://rasa.com/docs/rasa/conversation-driven-development/

Contact: Kristiina Jokinen kristiina.jokinen@aist.go.jp

<h2>2. How to</h2>

## Create virtual environment and test rasa model
First, create environment and install library fallow command.
```
conda create --name rasa_env_jp python==3.8  
```

Install library
```
pip install -r requirements.txt
```

Activate environment
```
conda activate rasa_env_jp
```

Train the model using following command;
```
rasa train
```

Run the action server using following command;
```
rasa run actions
```

Loads trained model and talk to assistant on the command line.
```
rasa shell
```

## Example questions for the demo
1. **Wikipedia:**
    ウィキペディアで{Question}を調べてください
2. **News:**
    ニュース
    (Topics)のニュース
3. **Diseases**:
    (disease)はどんな病気？
    (disease)の原因は何ですか？
    (disease)の症状は何ですか？
4. **Exercise domain**
    運動したい
    運動が終わりました
    etc...

<br>
<h2>3. References</h2>

On the whole project:<br>
Jokinen, K., Homma, K., Matsumoto, Y., Fukuda, K. (2022). Integration and Interaction of Trustworthy AI in a Virtual Coach – An Overview of EU-Japan Collaboration on Eldercare. In: Takama, Y. et al. (eds.): Advances in Artificial Intelligence – Selected Papers from the Annual Conference of Japanese Society of Artificial Intelligence (JSAI 2021). Advances in Intelligent Systems and Computing, vol 1423, Springer, Cham. pp.190-200.
<br>
paper: https://doi.org/10.1007/978-3-030-96451-1_17
<br>
video: https://www.youtube.com/watch?v=BaqDMmcLcmE

Interation model concerning the whole project:<br>
McTear M, Jokinen K, Alam MM, Saleem Q, Napolitano G, Szczepaniak F, Hariz M, Chollet G, Lohr C, Boudy J, Azimi Z, Roelen SD, Wieching R. Interaction with a Virtual Coach for Active and Healthy Ageing. Sensors. 2023; 23(5):2748. 
<br>
https://doi.org/10.3390/s23052748
