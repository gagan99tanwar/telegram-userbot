import random

REPLY_MAP = {

"hi": [
"Hello 👋","Hii 😄","Heyy","Wassup","Aagaye aap 😌",
"Hello ji 👋","Namaste 😌","Hey bro","Kaise ho","Kya haal"
],

"hello": [
"Hello 👋","Hii 😄","Heyy","Wassup","Aagaye aap 😌",
"Hello ji 👋","Namaste 😌","Hey bro","Kaise ho","Kya haal"
],

"aur batao": [
"Bas zinda hu 😭",
"Sab badhiya",
"Tum sunao",
"Kuch khas nahi",
"Bakchodi chal rahi hai",
"Aur kya scene hai",
"Same old life 😭",
"Sab mast",
"Bas timepass",
"Jee rahe hain"
],

"kya karte ho": [
"Timepass expert hu 😭",
"Padhai aur regret",
"Coding aur rona",
"Bas survive kar raha hu",
"Kuch productive nahi 😂",
"Life barbaad kar raha hu 😭",
"Khud ko busy dikhata hu",
"Bakchodi karta hu",
"Online rehta hu",
"Sab karta hu thoda thoda"
],

"kaha se ho": [
"UP se",
"Meerut side",
"India se 🇮🇳",
"Earth se 🌍",
"Secret location 🤫",
"Dilli ke aas paas",
"Yahi kahi se",
"Hidden base",
"Location confidential",
"Map me hu 😭"
],

"study": [
"Padh lo beta 😭",
"Exam aa rahe hain",
"Notes complete hue?",
"Assignment submit kiya?",
"Result ka wait hai",
"Revision hua kya",
"Teacher pakad lega 😂",
"Syllabus khatam hua?",
"Topper banoge kya",
"Attendance ka kya scene hai"
],

"neet": [
"Selection ho jayega 😭",
"Padhai kar le bhai",
"NEET ne sabko rulaya hai",
"Mock test diya kya",
"Revision kar lo",
"Dropper ho kya 😭",
"Rank aa jayegi",
"Bas consistency rakho",
"Pressure mat lo",
"All the best 😌"
],

"coding": [
"Bug mil gaya kya 😭",
"Deploy mat tod dena",
"Railway fir ro raha hoga 😂",
"Code chal gaya kya 👀",
"Syntax error spotted 😭",
"Git push kar diya?",
"Commit message kya tha 😂",
"Server down mat kar dena",
"Console kya bol raha hai?",
"Logs check karo"
],

"code": [
"Bug mil gaya kya 😭",
"Deploy mat tod dena",
"Railway fir ro raha hoga 😂",
"Code chal gaya kya 👀",
"Syntax error spotted 😭",
"Git push kar diya?",
"Commit message kya tha 😂",
"Server down mat kar dena",
"Console kya bol raha hai?",
"Logs check karo"
],

"bot": [
"Bot fir drama kar raha hai 😭",
"Restart karo",
"Deploy kar do",
"Config dekh lo",
"Logs check karo",
"Auto reply ka scene kya hai",
"Bot so gaya kya",
"Railway dekh lo",
"Environment variable check karo",
"Bot ko chai pilao 😭"
],

"admin": [
"Admin so rahe hain 😭",
"Owner ko tag karo",
"Admin power 😌",
"Meeting bulao admin ki",
"Kaun admin bana isko 😂",
"Report kar diya kya",
"Ban hammer ready hai 😭",
"Admin active karo",
"Admin discussion chal rahi hai",
"Power abuse mat karo 😂"
],

"vc": [
"VC me aao 😭",
"Mic on rakhna",
"Koi gaana lagao",
"VC ka mood nahi",
"Voice reveal 😭",
"Speaker on karo",
"Aur sunao",
"Sunne aa jao",
"Gaana mast tha",
"Join karo VC"
],

"photo": [
"Permission lo pehle 😏",
"Confidential file hai",
"Nahi milegi 😂",
"Secret hai",
"Pic locked 🔒",
"Itni bhi kya jaldi 👀",
"Photo premium feature hai 😭",
"Owner se approval lo",
"Gallery private hai",
"Nice try 😂"
],

"crush": [
"Naam batao 👀",
"Scene chal raha hai 😭",
"Dil ka mamla lagta hai",
"Confession kab hai",
"Story interesting hai",
"Crush spotted 😂",
"Love angle aa gaya",
"Ye friendship nahi lagti 😭",
"Red flag ya green flag 👀",
"Update dete rehna"
],

"love": [
"Love is temporary 😭",
"Dil toot jayega",
"Good luck soldier",
"Risky game",
"Red flag check karo",
"Strong feelings lag rahe hain",
"Ye serious ho gaya",
"Shubhkamnaye 😭",
"Scene set hai",
"Best of luck 😂"
],

"dhoka": [
"Trust issues 📈",
"Sab dete hain 😭",
"Dil sambhal ke",
"Expected tha",
"Ye dukh khatam kyu nahi hota",
"Life lesson mil gaya",
"Character development 😭",
"Sad moment",
"Recover ho jaoge",
"Karma dekhega"
],

"bimar": [
"Take care 🫂",
"Rest kar lo",
"Medicine le lo",
"Jaldi theek ho jao",
"Pani piyo",
"Doctor ko dikha lo",
"Aaram karo",
"Health first 😌",
"Get well soon 😭",
"Stress mat lo"
]
}

FALLBACK_REPLIES = [
"Acha 👀",
"Real 😭",
"Mood 😭",
"Fir kya hua",
"Waah bhai",
"Sach me?",
"Interesting 🤔",
"Kuch bhi 😂",
"Us moment 🫂",
"Lmao 😭",
"Bhai 😭",
"Chal jhoothe",
"Kya scene hai",
"Haan vo to hai",
"Samajh raha hu 😭",
"Ye unexpected tha",
"Full bakchodi chal rahi hai",
"Maza aa gaya 😂",
"Legend behaviour",
"Ye to personal ho gaya",
"Bas yahi dekhna baaki tha",
"Level alag hai 😭",
"Scene garam hai 👀",
"Hasa diya 😂",
"Control 😭",
"Are wah",
"Bilkul sahi",
"Matlab kuch bhi",
"Heavy baat kar di",
"Ab maja aayega"
def get_reply(message):
    msg = message.lower()

    for keyword, replies in REPLY_MAP.items():
        if keyword in msg:
            return random.choice(replies)

    return random.choice(FALLBACK_REPLIES)
    ]
