#!/usr/bin/env python3
"""Fill the remaining Ephesians gaps with notes written for BibleScroll.

Two gaps are left after Calvin and Meyer:

  explain  8 verses Calvin passes over (1:2, 1:6, 3:6, 3:21, 5:7, 5:10,
           6:6, 6:22)
  apply    all 155 verses — neither source carries reflection questions

These are written rather than sourced, from a Lutheran reading: law and
gospel distinguished, righteousness received rather than achieved,
assurance located in Christ instead of in the believer, and ordinary
work treated as calling. They are tagged source 'l' so the drawer can
say where they came from.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_book_data import smart_trim, EXPLAIN_MAX, TAKEAWAY_MAX

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

EXPLAIN = {
    '1:2': "<strong>Grace be to you, and peace, from God our Father</strong> "
           "(χάρις ὑμῖν καὶ εἰρήνη, <em>charis hymin kai eirēnē</em>)—The order is "
           "never reversed. <em>Charis</em> is God's favour toward us for Christ's "
           "sake, not a quality poured into us; <em>eirēnē</em> is what that favour "
           "creates, the quieted conscience that knows God is no longer against it. "
           "Peace is therefore not a mood to be worked up but a verdict to be "
           "received.<br><br>Father and Lord Jesus Christ are named as one source. "
           "Grace has no second fountain.",

    '1:6': "<strong>Wherein he hath made us accepted in the beloved</strong> "
           "(ἐχαρίτωσεν ἡμᾶς ἐν τῷ ἠγαπημένῳ, <em>echaritōsen hēmas</em>)—The verb "
           "is past and passive: acceptance is something done to us, outside us, "
           "already finished. And it is located <em>in the Beloved</em>, not in the "
           "believer. We are received as the Son is received, because we are found "
           "in him.<br><br>This is why assurance looks away from itself. Examine "
           "your love and you will find it cold; look to Christ and you find God's "
           "verdict already spoken.",

    '3:6': "<strong>That the Gentiles should be fellowheirs, and of the same "
           "body</strong> (συγκληρονόμα καὶ σύσσωμα, <em>synklēronoma kai "
           "syssōma</em>)—Paul coins three words beginning with <em>syn-</em>, "
           "\"together with\": co-heirs, co-body, co-sharers. Gentiles are not "
           "admitted to the edge of Israel's blessing; they are given the whole of "
           "it.<br><br>What makes them one is named last — <em>by the gospel</em>. "
           "The church is not a society formed by agreement or ancestry. It exists "
           "wherever that word is preached and believed.",

    '3:21': "<strong>Unto him be glory in the church by Christ Jesus</strong> "
            "(ἐν τῇ ἐκκλησίᾳ καὶ ἐν Χριστῷ Ἰησοῦ)—Glory is returned to God in two "
            "places at once: in the church and in Christ. The church has no glory "
            "of its own to offer; what it gives back is what it first received in "
            "the Son.<br><br>\"Throughout all ages, world without end\" renders a "
            "Hebraism piled up for emphasis. Paul ends the letter's doctrinal half "
            "not with a conclusion but with doxology — the proper response to grace "
            "is praise, not analysis.",

    '5:7': "<strong>Be not ye therefore partakers with them</strong> "
           "(μὴ οὖν γίνεσθε συμμέτοχοι αὐτῶν, <em>mē oun ginesthe</em>)—Everything "
           "hangs on <em>therefore</em>. Paul does not open with the command; he "
           "reasons forward from what the Ephesians already are — \"now are ye "
           "light in the Lord\" (v. 8).<br><br>Law spoken this way does not "
           "threaten a standing, it describes one. The warning is real, but its "
           "force is: do not go on living as what you no longer are.",

    '5:10': "<strong>Proving what is acceptable unto the Lord</strong> "
            "(δοκιμάζοντες τί ἐστιν εὐάρεστον τῷ κυρίῳ, <em>dokimazontes</em>)—"
            "<em>Dokimazō</em> is the word for testing metal to see whether it is "
            "genuine. Paul assumes a Christian life with real discretion in it: not "
            "a rulebook covering every case, but a mind trained by the gospel, "
            "weighing what actually pleases God here.<br><br>A work is acceptable "
            "because the person is already accepted (1:6). Faith makes the doer "
            "pleasing first; only then the deed.",

    '6:6': "<strong>Not with eyeservice, as menpleasers; but as the servants of "
           "Christ</strong> (μὴ κατ' ὀφθαλμοδουλίαν, <em>mē kat' "
           "ophthalmodoulian</em>)—Paul appears to have coined "
           "<em>ophthalmodoulia</em>, \"eye-service\": work done only while "
           "watched. Against it he sets work done <em>from the heart</em> for a "
           "Master who is never not watching.<br><br>This lifts ordinary labour "
           "into calling. The slave sweeping a floor and the apostle writing the "
           "letter serve the same Lord. The station differs; the service does not.",

    '6:22': "<strong>That he might comfort your hearts</strong> "
            "(παρακαλέσῃ τὰς καρδίας ὑμῶν, <em>parakalesē tas kardias</em>)—"
            "<em>Parakaleō</em> is the verb behind <em>Paraclete</em>: to come "
            "alongside and hearten. Tychicus carries no new revelation. He carries "
            "news, and his errand is comfort.<br><br>A letter about cosmic powers "
            "and the whole armour of God ends with one man sent to steady a few "
            "anxious congregations. The consolation of brothers is itself a way the "
            "gospel arrives.",
}

APPLY = {
    # ---- Chapter 1: the blessing already given ----
    '1:1': "Paul calls ordinary church members \"saints\" before naming a single virtue of theirs. What changes if holiness is a status Christ gives rather than a rank you climb toward?",
    '1:2': "Paul always puts grace before peace, never the reverse. Where are you trying to find peace without first receiving grace?",
    '1:3': "\"All spiritual blessings\" is past tense and already yours. What are you still asking God for that he says you already have in Christ?",
    '1:4': "Election is raised here to comfort, not to unsettle. When you think about God choosing, does it drive you to Christ or to speculation about yourself?",
    '1:5': "Adoption means God wanted you, not merely tolerated you. How would today look if you believed God's disposition toward you was \"good pleasure\"?",
    '1:6': "Your acceptance is located in Christ, not in your performance. Whose record are you checking when you wonder whether God is pleased with you?",
    '1:7': "Redemption is priced by blood, not by your improvement. Which sin are you still trying to pay for yourself?",
    '1:8': "Grace is described as abounding, not rationed. Where do you treat God's mercy as a limited supply you might use up?",
    '1:9': "God's will here is revealed, not hidden. Are you hunting for a secret will of God while ignoring the one he has published in Christ?",
    '1:10': "All things are being gathered up into Christ. Which part of your life do you quietly treat as outside that gathering?",
    '1:11': "An inheritance is received, never earned. What would change if you stopped negotiating with God and started receiving from him?",
    '1:12': "Paul says the point of your salvation is God's praise. Whose glory is your faith actually organised around?",
    '1:13': "Faith came by hearing a word, not by producing an inner experience. Where is that word reaching you regularly?",
    '1:14': "The Spirit is called a down payment, not the whole sum. How does knowing the best is still ahead change what you can endure now?",
    '1:15': "Paul hears of faith and love together, as one report. Which of the two is more visible in you this week?",
    '1:16': "Paul's first instinct toward this church is thanksgiving. Who could you thank God for instead of criticising?",
    '1:17': "Paul prays for knowledge of a person, not mastery of a subject. Do you want to know about God, or to know him?",
    '1:18': "Paul assumes Christians need their eyes opened to what they already possess. What do you know to be true but do not yet see?",
    '1:19': "The power named here is aimed at believers, not withheld from them. Where have you decided God's power does not reach?",
    '1:20': "The measure of God's power toward you is the resurrection. What situation are you treating as more final than a grave?",
    '1:21': "Christ sits above every power that frightens you. Name the one you fear most — where does it sit relative to him?",
    '1:22': "Christ rules everything for the church's sake. How does that reframe the headlines that unsettle you?",
    '1:23': "The church is called Christ's body, not his project. How should that change the way you speak about your congregation?",

    # ---- Chapter 2: dead, then raised ----
    '2:1': "Paul's diagnosis is death, not weakness. Why can a dead man contribute nothing toward his own rescue?",
    '2:2': "Sin is pictured as following a current, not choosing a direction. Where are you drifting without ever deciding?",
    '2:3': "\"By nature\" makes this a condition, not a comment on your bad days. Does that humble you or offend you?",
    '2:4': "Everything turns on two words: \"But God.\" Which sentence about your life needs that interruption?",
    '2:5': "God acted while you were dead — before any response was possible. What does that do to the idea that you met him halfway?",
    '2:6': "You are already seated with Christ. How would you pray differently if you prayed from that seat rather than toward it?",
    '2:7': "God saves you partly to exhibit his kindness for ages to come. Are you an exhibit of his mercy or of your own effort?",
    '2:8': "Even the faith is a gift. What have you quietly been counting as your own contribution?",
    '2:9': "Boasting is the stated reason works are excluded. What do you most want credit for in front of God?",
    '2:10': "Good works come after being created in Christ, never before. Are your works trying to secure something, or to spend something?",
    '2:11': "Paul commands you to remember what you once were. What does forgetting that do to your patience with other people?",
    '2:12': "This is the honest description of life outside Christ — no hope, and without God. Do you still envy it?",
    '2:13': "The distance was closed by blood, not by your approach. Where are you still behaving like an outsider?",
    '2:14': "Christ is not a peace-broker; he is our peace. Which wall are you maintaining that he has already demolished?",
    '2:15': "God's solution was not to improve two groups but to make one new humanity. Which identity do you hold more tightly than \"in Christ\"?",
    '2:16': "Reconciliation with God and with each other happen at the same cross. Can you claim the first while refusing the second?",
    '2:17': "Christ preaches peace to those far off first. Who is \"far off\" in your world, and have you announced peace to them?",
    '2:18': "Access runs through the Son, by the Spirit, to the Father. How should that shape the way you begin praying?",
    '2:19': "You hold citizenship, not a visa. Where do you still relate to God's people as a guest?",
    '2:20': "The church rests on an apostolic word, not on current opinion. What are you building on that will not hold weight?",
    '2:21': "The temple is still under construction. How should that change your impatience with the church's flaws — and your own?",
    '2:22': "God's dwelling is a \"builded together,\" not a solitary heart. What does that say about gathering with others?",

    # ---- Chapter 3: the mystery made public ----
    '3:1': "Paul calls himself Christ's prisoner, not Rome's. Which circumstance would you describe differently if you named Christ as the one holding you?",
    '3:2': "Paul treats his ministry as a stewardship of grace. What has God handed you to administer rather than to own?",
    '3:3': "The gospel came to Paul by revelation, not discovery. Where are you trying to reason your way to something God must reveal?",
    '3:4': "Paul expects ordinary readers to understand him. What actually keeps you from reading Scripture for yourself?",
    '3:5': "What was hidden for ages has now been published. How should that make you bolder about what is plain?",
    '3:6': "The word is \"fellow\" three times over — equal share, not junior membership. Whom do you treat as a lesser partner in the gospel?",
    '3:7': "Paul's qualification is a gift, not a résumé. What service are you avoiding because you feel unqualified?",
    '3:8': "Paul's estimate of himself got lower as his ministry grew. What does that pattern suggest about spiritual maturity?",
    '3:9': "The mystery is now meant to be seen by all. Whom have you assumed is beyond explaining it to?",
    '3:10': "The church is God's display to unseen powers. Does your congregation seem that significant to you on a normal Sunday?",
    '3:11': "None of this was improvised. What in your life feels accidental that God calls purposed?",
    '3:12': "Confidence before God rests on Christ's faithfulness, not your sincerity. Do you approach God boldly or apologetically?",
    '3:13': "Paul worries about their discouragement, not his own chains. Whose suffering tempts you to lose heart?",
    '3:14': "Paul's response to doctrine is to kneel. When did truth last drive you to prayer rather than to argument?",
    '3:15': "Your family name comes from the Father. Which name do you actually live under day to day?",
    '3:16': "The strengthening Paul asks for is inward and hidden. What would inner strength look like in your life this week?",
    '3:17': "Christ dwells by faith, not by feeling. How does that steady you on a day when you feel nothing?",
    '3:18': "Even comprehension is a group activity here — \"with all saints.\" What have you understood only because someone helped you see it?",
    '3:19': "Paul prays you would know what cannot be fully known. Where have you settled for a manageable God?",
    '3:20': "God's capacity exceeds your imagination, not merely your request. What are you asking too small?",
    '3:21': "Glory is returned to God in the church. What does your gathering actually return to him?",

    # ---- Chapter 4: one body, walking worthy ----
    '4:1': "The calling comes first, the walking after. Are you walking to earn a calling, or from one already given?",
    '4:2': "Lowliness, meekness, longsuffering, forbearing — every one is a cost paid toward another person. Which costs you most right now?",
    '4:3': "Unity is kept, not manufactured; the Spirit already made it. What are you tempted to break that you did not build?",
    '4:4': "Paul argues for unity from what is already one. Which of these \"ones\" do you most often forget?",
    '4:5': "Your baptism is named alongside the Lord himself. How often do you think of it as something God did to you?",
    '4:6': "God is above all, through all, and in you all. Which of those three do you most need to hear today?",
    '4:7': "Every single member is given grace and a gift. What is yours, and where is it going unused?",
    '4:8': "Christ's victory results in gifts distributed, not hoarded. What has his victory put into your hands?",
    '4:9': "The ascent required a descent first. Where do you want glory without the lowering that comes before it?",
    '4:10': "There is no place Christ does not fill. Where do you behave as though he were absent?",
    '4:11': "Preachers are Christ's gift to the church, not its employees. How should that shape the way you listen on Sunday?",
    '4:12': "The ministry exists to equip the saints for ministry. What work is yours that no pastor can do for you?",
    '4:13': "Maturity is measured by Christ's stature, not by comparison with others. Whom are you measuring yourself against?",
    '4:14': "Doctrine is presented here as ballast against manipulation. What teaching have you accepted without ever testing it?",
    '4:15': "Truth and love are one act here, not a balance to strike. Which of the two do you tend to sacrifice?",
    '4:16': "The body grows only as each joint supplies something. What does the body go without when you withdraw?",
    '4:17': "Paul locates the problem in the mind first. What thinking has to change before your behaviour will?",
    '4:18': "Ignorance here is a condition of the heart, not a lack of information. Where do you know better and still choose otherwise?",
    '4:19': "A conscience can go numb by repetition. What have you stopped feeling guilty about that should still trouble you?",
    '4:20': "Christ himself is the curriculum — you learn him, not just about him. What have you learned that actually changed how you live?",
    '4:21': "Truth is located in a person: \"the truth is in Jesus.\" How does that differ from treating Christianity as a set of positions?",
    '4:22': "The old self is called corrupt and deceitful — it lies to you. What is it promising you at the moment?",
    '4:23': "Renewal is ongoing and inward. What daily input is shaping your mind more than the Word is?",
    '4:24': "The new self is created, not self-improved. What are you trying to renovate that God intends to replace?",
    '4:25': "The reason given for honesty is membership: \"we are members one of another.\" How does lying to a fellow Christian injure you too?",
    '4:26': "Anger itself is not forbidden; letting it settle in is. What anger have you allowed to stay overnight?",
    '4:27': "Unresolved anger is called an opening for the devil. Which door have you left ajar?",
    '4:28': "The thief's cure is not merely stopping but giving. How is your work aimed at somebody else's need?",
    '4:29': "Speech is meant to deliver grace to whoever hears it. Did your words yesterday give anyone grace?",
    '4:30': "The Spirit can be grieved, yet the seal holds. Why do both halves of that sentence matter?",
    '4:31': "Bitterness heads the list, ahead of wrath and malice. What are you still holding that began as something small?",
    '4:32': "The standard is not fairness but the forgiveness you received. Whom does that name for you?",

    # ---- Chapter 5: light, wisdom, and the household ----
    '5:1': "Imitation flows from being \"dear children,\" not from earning the title. Do you imitate God as a child or as an employee?",
    '5:2': "Christ's love is defined by self-giving. What would love cost you this week if it looked like that?",
    '5:3': "Paul sets the bar at \"not once named among you.\" Where have you grown comfortable discussing what you should be avoiding?",
    '5:4': "Thanksgiving is offered as the replacement for coarse talk. What would gratitude displace in your speech?",
    '5:5': "Covetousness is called idolatry outright. What do you want so badly that it functions as a god?",
    '5:6': "Some words exist to make sin sound safe. Which phrase have you used to soften something?",
    '5:7': "The command rests on a \"therefore\" — on who you already are. What behaviour no longer fits your identity?",
    '5:8': "Paul says you were darkness, not merely in it. How does that make the change more radical than you thought?",
    '5:9': "Fruit grows; it is not manufactured. What are you straining to produce that only the Spirit can grow?",
    '5:10': "Paul expects you to weigh what pleases God, not just follow rules. Which decision needs that discernment now?",
    '5:11': "Darkness is called unfruitful — it produces nothing. What has sin actually yielded you?",
    '5:12': "Secrecy is treated here as evidence. Is there something you do only when unobserved?",
    '5:13': "Light exposes in order to heal, not to humiliate. What are you keeping in the dark out of fear?",
    '5:14': "The command to wake comes attached to a promise of light. Where do you need rousing?",
    '5:15': "Wisdom here is about how you walk, not what you know. Where are you living carelessly?",
    '5:16': "Time is something to be bought back. What is consuming hours you would want returned?",
    '5:17': "God's will is presented as knowable. Have you looked for it where he has actually revealed it?",
    '5:18': "Both drunkenness and the Spirit are about what controls you. What are you currently using to manage your inner life?",
    '5:19': "Singing is listed as a way Christians preach to one another. What has a hymn taught you that a sermon did not?",
    '5:20': "This thanksgiving has no exemptions — \"always for all things.\" What is hardest to give thanks for right now?",
    '5:21': "Mutual submission heads the whole household section. Where would deference cost you most?",
    '5:22': "The measure is \"as unto the Lord,\" which both dignifies this and limits it. How does that guard against misuse of the verse?",
    '5:23': "Headship is defined by Christ, who is the saviour of the body. What kind of headship does that rule out?",
    '5:24': "The church's response to Christ is the pattern held up here. What makes Christ worth trusting that way?",
    '5:25': "The husband's command is to die, not to rule. Where does that reshape what you thought this passage taught?",
    '5:26': "Water and word together — the language of baptism. How does that describe what God has already done to you?",
    '5:27': "The church's beauty is what Christ produces, not what it brings him. Where do you expect the church to earn its worth?",
    '5:28': "Love is measured against instinctive self-care. Are you as attentive to another as you are to yourself?",
    '5:29': "Nourish and cherish describe Christ's ongoing care for his church. Which of the two do you need from him today?",
    '5:30': "Union with Christ is put in bodily terms, not merely metaphor. What does belonging to him that closely mean?",
    '5:31': "Marriage is quoted from Genesis in order to explain Christ. What does that say about how seriously God takes it?",
    '5:32': "Paul says marriage was always pointing somewhere beyond itself. Does your marriage — or your singleness — point there?",
    '5:33': "Paul ends a passage about a great mystery with \"every one of you in particular.\" Which general truth do you need to make particular?",

    # ---- Chapter 6: household, armour, and farewell ----
    '6:1': "Obedience is framed \"in the Lord,\" not absolutely. How does that both require it and limit it?",
    '6:2': "Honour outlasts obedience — it applies at every age. How do you honour your parents now?",
    '6:3': "The promise attached is ordinary blessing, not payment. How does God tie our good to his commands without making them a wage?",
    '6:4': "Fathers are warned about exasperating, not only about neglecting. What in your manner provokes rather than forms?",
    '6:5': "The lowest station in the household is addressed as serving Christ directly. What does that do to the idea of menial work?",
    '6:6': "Paul coins a word for work done only while watched. Who are you when nobody checks?",
    '6:7': "Attitude is commanded alongside action. Which of your duties needs a changed attitude more than changed effort?",
    '6:8': "Unnoticed good is not unnoticed by God. What faithfulness of yours has gone unseen?",
    '6:9': "Authority is told to serve under a higher Master, with no respect of persons. Where does your authority need that check?",
    '6:10': "The strength commanded is borrowed, not summoned. How do you actually draw on strength that is not your own?",
    '6:11': "The armour is God's, given to you to put on. Which piece are you trying to fight without?",
    '6:12': "Your real opponent is not the person who angers you. How would naming the true enemy change that conflict?",
    '6:13': "The goal stated is to stand, not to advance. What would simply standing require of you now?",
    '6:14': "The righteousness worn over the heart is Christ's. What are you defending yourself with instead — your own record?",
    '6:15': "Even the footing is gospel. What ground are you actually standing on when you are pressed?",
    '6:16': "Faith is defensive here — it receives rather than achieves. Which accusation does faith answer for you?",
    '6:17': "The only offensive weapon in the list is a word. Do you know it well enough to use it?",
    '6:18': "The armour passage ends in prayer for other people. Who needs your prayer more than your opinion?",
    '6:19': "Even Paul asks for words to be given him. What would you ask God to help you say?",
    '6:20': "Paul holds an ambassador's office while in chains. What limitation are you treating as a disqualification?",
    '6:21': "Paul names a brother most readers would never meet. Who serves quietly in your church without being named?",
    '6:22': "The letter ends on an errand of comfort. Whose heart could you steady this week?",
    '6:23': "Peace, love and faith are all said to come from God the Father. Which are you trying to generate yourself?",
    '6:24': "The letter opens with grace and closes with grace. What does it mean that grace frames everything in between?",
}


def main():
    path = os.path.join(DATA, 'study_Ephesians.json')
    with io.open(path, encoding='utf-8') as fh:
        study = json.load(fh)

    missing = sorted(set(study) - set(APPLY))
    if missing:
        raise SystemExit('no reflection question for: %s' % ', '.join(missing))
    extra = sorted(set(APPLY) - set(study))
    if extra:
        raise SystemExit('question for verses that do not exist: %s' % ', '.join(extra))

    for key, text in EXPLAIN.items():
        entry = study[key]
        if entry['explain'].strip():
            raise SystemExit('%s already has commentary; refusing to overwrite' % key)
        entry['explain'] = smart_trim(text, EXPLAIN_MAX)
        entry['takeaway'] = smart_trim(entry['explain'], TAKEAWAY_MAX)
        entry['srcExplain'] = 'l'

    for key, text in APPLY.items():
        study[key]['apply'] = text

    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(study, ensure_ascii=False, separators=(', ', ': ')))
    print('Ephesians: filled %d commentaries and %d reflection questions'
          % (len(EXPLAIN), len(APPLY)))


if __name__ == '__main__':
    main()
