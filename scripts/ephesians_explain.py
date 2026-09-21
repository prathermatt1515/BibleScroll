#!/usr/bin/env python3
"""Ephesians commentary written for BibleScroll, from a Lutheran reading.

kjvstudy.org left Ephesians as an unfilled template, so its Explain text came
from Calvin. Calvin is sound but reads as 16th-century prose, heavy going in a
one-verse-at-a-time feed, so these replace him for the whole book.

The reading throughout: law and gospel distinguished, righteousness received
rather than achieved, election and assurance located in Christ instead of in
the believer's own state, the means of grace as where God actually deals with
us, and ordinary work treated as calling.

Chapters 1-3 live here; chapters 4-6 in ephesians_explain_2.py.
"""

NOTES = {
    # ---- Chapter 1: blessing, election, and the sealed inheritance ----
    '1:1': "<strong>Paul, an apostle of Jesus Christ by the will of God</strong> (ἀπόστολος Χριστοῦ Ἰησοῦ διὰ θελήματος θεοῦ)—Paul's office rests on God's will, not on his own ambition or the congregation's vote. An apostle is a sent one; the authority lies wholly in the sending.<br><br>He then calls his readers <em>saints</em> (ἁγίοις, <em>hagiois</em>) before commending a single virtue of theirs. Holiness here is a standing conferred by Christ, not a rank reached by effort — which is why a whole congregation, rather than an elite within it, can be addressed this way.",

    '1:3': "<strong>Who hath blessed us with all spiritual blessings in heavenly places in Christ</strong> (ἐν τοῖς ἐπουρανίοις ἐν Χριστῷ)—The verb is past tense: the blessing is done, not pending. <em>All</em> leaves nothing to be added later by our performance.<br><br>Everything Paul is about to list — election, adoption, redemption, the seal of the Spirit — is located <em>in Christ</em>. Outside him there is no fragment of it; inside him no part is withheld. The Christian's wealth is therefore never visible when he looks at himself.",

    '1:4': "<strong>According as he hath chosen us in him before the foundation of the world</strong> (ἐξελέξατο ἡμᾶς ἐν αὐτῷ)—Election is raised here as comfort, not as a puzzle to be solved. Notice where the choosing happens: <em>in him</em>. God's choice is not a hidden decree to be pried open but a choice made in Christ, and so found in Christ.<br><br>This is why an anxious conscience should not search the eternal will for its own name. Look to Christ, and you are looking at the place where the choosing was done.",

    '1:5': "<strong>Having predestinated us unto the adoption of children</strong> (προορίσας ἡμᾶς εἰς υἱοθεσίαν, <em>huiothesian</em>)—<em>Huiothesia</em> was a Roman legal act: a child taken in, given the family name, made heir with full right. Nothing in the adopted child prompts it.<br><br>The ground is named plainly — <em>according to the good pleasure of his will</em>. Not our foreseen merit, not reluctance overcome by persuasion, but his pleasure. God is not talked into loving us. He is glad to.",

    '1:7': "<strong>In whom we have redemption through his blood, the forgiveness of sins</strong> (ἀπολύτρωσιν διὰ τοῦ αἵματος αὐτοῦ)—<em>Apolytrōsis</em> is release secured by a ransom paid. Paul immediately says what the release consists of: the forgiveness of sins. Redemption is not a vague improvement in our prospects but the cancelling of guilt.<br><br>And it is measured <em>according to the riches of his grace</em> — by God's abundance rather than by the size of the debt or the sincerity of the debtor.",

    '1:8': "<strong>Wherein he hath abounded toward us in all wisdom and prudence</strong> (ἐπερίσσευσεν εἰς ἡμᾶς)—<em>Perisseuō</em> means to overflow, to run past the brim. Grace is not measured out against need; it exceeds it.<br><br>The wisdom and prudence here are God's, not ours — the wisdom with which he planned and carried through our rescue. Paul is not praising clever believers but a God whose plan was neither improvised nor grudging.",

    '1:9': "<strong>Having made known unto us the mystery of his will</strong> (τὸ μυστήριον τοῦ θελήματος αὐτοῦ)—A <em>mystērion</em> in Paul is not a riddle that resists solving but a secret God has now told. The weight falls on <em>made known</em>.<br><br>This guards against a restless religion forever hunting God's hidden will. What God intends for you he has published in Christ. Where he has spoken, listen; where he has not, he has not asked you to guess.",

    '1:10': "<strong>That he might gather together in one all things in Christ</strong> (ἀνακεφαλαιώσασθαι τὰ πάντα ἐν τῷ Χριστῷ)—<em>Anakephalaiōsasthai</em> means to sum up, to bring under one head, as a column of figures is totalled.<br><br>The scope is <em>things in heaven and things on earth</em>. Christian hope is therefore not escape from creation but its gathering up. Nothing God made is written off; it is brought under the one head able to hold it.",

    '1:11': "<strong>In whom also we have obtained an inheritance</strong> (ἐκληρώθημεν)—The verb comes from the casting of lots: a portion assigned rather than earned. Paul at once adds that God <em>worketh all things after the counsel of his own will</em>.<br><br>That sentence is meant to steady, not to frighten. The one arranging all things is the Father who adopted you. Providence is not impersonal machinery; it is the working of the very will that chose you in Christ.",

    '1:12': "<strong>That we should be to the praise of his glory</strong> (εἰς ἔπαινον δόξης αὐτοῦ)—This refrain closes each movement of the paragraph. The end of salvation is not first our comfort but God's praise, and our comfort follows precisely because his glory lies in showing mercy.<br><br>A faith organised around our own flourishing will always be unstable, because it makes us the point. Here the point is somewhere else, and that is the relief.",

    '1:13': "<strong>After that ye heard the word of truth... ye were sealed</strong> (ἐσφραγίσθητε τῷ πνεύματι)—Faith arrives by hearing, not by introspection. The order is plain: heard, believed, sealed.<br><br>A <em>sphragis</em> was an owner's mark, proof of possession and guarantee of safe delivery. The Spirit is not a reward for the advanced but God's mark on everyone who believes the word — which is why assurance rests on the promise heard rather than on the strength of the hearing.",

    '1:14': "<strong>Which is the earnest of our inheritance</strong> (ἀρραβὼν τῆς κληρονομίας ἡμῶν)—<em>Arrabōn</em> was a commercial term: a deposit that both guarantees the remainder and is itself part of it. The Spirit is not a substitute for what is coming but its first instalment.<br><br>So present experience of God is real but partial. Expect neither nothing now nor everything now. What you have is genuine, and it is a down payment.",

    '1:15': "<strong>After I heard of your faith in the Lord Jesus, and love unto all the saints</strong>—Paul receives one report with two halves. Faith fastens on Christ; love spills toward the saints. Neither is offered as evidence that the other may be skipped.<br><br>Notice the directions. Faith goes upward and receives; love goes outward and gives. Reverse them — faith in ourselves, love toward God as a way of earning — and the gospel is lost.",

    '1:16': "<strong>Cease not to give thanks for you, making mention of you in my prayers</strong>—Paul's habitual response to other Christians is gratitude. He is writing to a church he will go on to instruct and correct, and he begins by thanking God for them.<br><br>Thanksgiving is not a warm preliminary here but a judgement about where their faith came from. You do not thank one person for what another achieved. Paul thanks God because God did it.",

    '1:17': "<strong>May give unto you the spirit of wisdom and revelation in the knowledge of him</strong> (ἐν ἐπιγνώσει αὐτοῦ)—<em>Epignōsis</em> is knowledge that engages the knower, not information held at a distance.<br><br>And observe that Paul prays for it. Understanding of God is a gift asked for, not a capacity we bring to the text. The same Spirit who sealed them must also open what the sealing means.",

    '1:18': "<strong>The eyes of your understanding being enlightened; that ye may know what is the hope of his calling</strong>—Paul prays that believers would see what they already own. The problem he addresses is not deficiency but blindness.<br><br>Much of the Christian life is exactly this: being brought to see what is already true. Not new gifts, but opened eyes; not more grace, but sight of the grace given.",

    '1:19': "<strong>And what is the exceeding greatness of his power to us-ward who believe</strong> (τὸ ὑπερβάλλον μέγεθος τῆς δυνάμεως αὐτοῦ)—Paul stacks words for power until the sentence nearly buckles under them. The point is the direction: <em>to us-ward</em>, toward believers.<br><br>That power is not held in reserve pending our improvement. It is already exerted toward those who believe — and its measure is given in the verse that follows.",

    '1:20': "<strong>Which he wrought in Christ, when he raised him from the dead</strong>—Here is the measuring rod for God's power toward you: not a storm calmed or a sea parted, but a corpse raised and enthroned.<br><br>This matters pastorally. Nothing you face has yet reached the difficulty of raising the dead, and that is the standard by which God's power toward you is gauged. Nothing in your life is more final than the grave he has already emptied.",

    '1:21': "<strong>Far above all principality, and power, and might, and dominion</strong> (ὑπεράνω πάσης ἀρχῆς)—Paul names the powers without pausing to explain them, then sets Christ above the lot — in this age and in the one to come.<br><br>He is not denying that such powers are real or frightening. He is placing them. The Christian is not told that nothing threatens, but that nothing threatening sits higher than the one who holds him.",

    '1:22': "<strong>And gave him to be the head over all things to the church</strong>—The government of everything is exercised <em>to the church</em>, for its sake. Christ does not rule the world in one capacity and love his people in another.<br><br>So a believer reads history, and the morning's news, as administered by the same hand that was pierced. Not that events are always explicable, but that they are not in other hands.",

    '1:23': "<strong>Which is his body, the fulness of him that filleth all in all</strong> (τὸ πλήρωμα τοῦ τὰ πάντα ἐν πᾶσιν πληρουμένου)—The church is called Christ's <em>body</em> and his <em>fulness</em>. He is incomplete without it — not from any lack in himself, but because he has chosen to be a head with members.<br><br>Which forbids treating the congregation as optional machinery for a private faith. Paul cannot finish describing Christ without mentioning the people he saved.",
}

NOTES.update({
    # ---- Chapter 2: dead, raised, and built together ----
    '2:1': "<strong>And you hath he quickened, who were dead in trespasses and sins</strong> (νεκροὺς τοῖς παραπτώμασιν)—The diagnosis is death, not illness or weakness. A sick man can call for help; a dead man cannot assist in his own raising.<br><br>This is the hinge the chapter turns on. Were we merely weakened, grace would be assistance. Since we were dead, grace must be resurrection — and resurrection is something done to you, never something done with your help.",

    '2:2': "<strong>Wherein in time past ye walked according to the course of this world</strong> (κατὰ τὸν αἰῶνα τοῦ κόσμου τούτου)—Sin is described as a current followed rather than a decision made. One walks with the age, and the walking feels like freedom.<br><br>Paul then names a power behind the current. The unbelieving life is not neutral ground where someone simply has not yet chosen; it is already occupied territory.",

    '2:3': "<strong>And were by nature the children of wrath, even as others</strong> (τέκνα φύσει ὀργῆς)—<em>Physei</em>, \"by nature\": a condition rather than a comment on particularly bad days. Paul includes himself and every reader in it.<br><br>The word <em>wrath</em> offends modern ears, but remove it and grace shrinks to politeness. God's settled opposition to what destroys his creatures is not a flaw in his love; it is love taken seriously.",

    '2:4': "<strong>But God, who is rich in mercy, for his great love wherewith he loved us</strong> (ὁ δὲ θεὸς πλούσιος ὢν ἐν ἐλέει)—Two words turn the whole paragraph. Everything before them described us; everything after describes God.<br><br>Observe that the cause is entirely in him — his mercy, his love — with nothing in us cited. Paul has just said we were dead. There was nothing in us to cite.",

    '2:5': "<strong>Even when we were dead in sins, hath quickened us together with Christ</strong> (συνεζωοποίησεν τῷ Χριστῷ)—The timing settles the question of who began: <em>when we were dead</em>. God acted before any response was possible.<br><br>Paul then interrupts his own sentence to say it outright — <em>by grace ye are saved</em> — as though he cannot wait three more verses. The parenthesis is the point of the paragraph.",

    '2:6': "<strong>And hath raised us up together, and made us sit together in heavenly places</strong> (συνήγειρεν καὶ συνεκάθισεν)—Both verbs are past. The Christian's seat is not a prospect but a present fact, held in Christ rather than in personal attainment.<br><br>So prayer is not petitioning from outside the door. It is speech from inside the room, by a right belonging to the one in whom we are seated.",

    '2:7': "<strong>That in the ages to come he might shew the exceeding riches of his grace</strong> (ἐνδείξηται τὸ ὑπερβάλλον πλοῦτος)—God's purpose in saving you runs past your relief. You are to be evidence, displayed for ages, of what his kindness does.<br><br>That is a strange sort of dignity: not a trophy of your progress but an exhibit of his mercy. The glory shown is his, and the ones showing it contributed nothing.",

    '2:8': "<strong>For by grace are ye saved through faith; and that not of yourselves: it is the gift of God</strong> (χάριτι... διὰ πίστεως)—Grace is the cause, faith the instrument. Faith saves not because believing is a fine quality but because of what it lays hold of.<br><br>The <em>that</em> in \"not of yourselves\" is neuter and takes in the whole transaction — grace, salvation, and the faith itself. Nothing is left for us to supply and then claim credit for.",

    '2:9': "<strong>Not of works, lest any man should boast</strong> (οὐκ ἐξ ἔργων, ἵνα μή τις καυχήσηται)—Paul gives the reason works are excluded, and it is not that works are worthless. It is that boasting must be excluded.<br><br>The urge to contribute is not humility; it is the wish to have something to say for oneself before God. Grace silences that, and the silence is where peace starts — a conscience with nothing to defend has nothing left to lose.",

    '2:10': "<strong>For we are his workmanship, created in Christ Jesus unto good works</strong> (αὐτοῦ γάρ ἐσμεν ποίημα)—Having excluded works as the cause, Paul restores them as the consequence. We are <em>created unto</em> them, not saved by them.<br><br>And they are <em>before ordained that we should walk in them</em> — prepared in advance, like a path laid out. Good works are not projects we invent to impress God but the road already under our feet.",

    '2:11': "<strong>Wherefore remember, that ye being in time past Gentiles in the flesh</strong>—Paul commands remembering. Forgetting what we were is not modesty about the past; it breeds contempt for people still standing where we once stood.<br><br>He also flags the labels — Uncircumcision and Circumcision, \"made by hands.\" Religious distinctions that people treated as ultimate are described here as human handiwork, and Christ has made them obsolete.",

    '2:12': "<strong>Having no hope, and without God in the world</strong> (ἐλπίδα μὴ ἔχοντες καὶ ἄθεοι ἐν τῷ κόσμῳ)—Paul piles up five negatives: without Christ, alien, stranger, no hope, without God. He does not soften the description of life outside the promise.<br><br>The honesty is pastoral. Only someone who has grasped what \"no hope\" meant can hear the \"but now\" of the next verse as more than a religious phrase.",

    '2:13': "<strong>But now in Christ Jesus ye who sometimes were far off are made nigh by the blood of Christ</strong>—The distance was not crossed by the far-off party. It was closed at cost, from the other side.<br><br>\"But now\" answers \"at that time\" in the previous verse. What changed is not our religious attainment but our location: <em>in Christ Jesus</em>. Everything Paul says about us depends on that address.",

    '2:14': "<strong>For he is our peace, who hath made both one</strong> (αὐτὸς γάρ ἐστιν ἡ εἰρήνη ἡμῶν)—Not that he makes peace, or teaches it; he <em>is</em> it. Peace between hostile groups is not a policy they adopt but a person they share.<br><br>The <em>middle wall of partition</em> would have brought to mind the barrier in the temple beyond which no Gentile could pass on pain of death. Paul says it is rubble.",

    '2:15': "<strong>For to make in himself of twain one new man, so making peace</strong> (ἕνα καινὸν ἄνθρωπον)—God's remedy was not to improve two groups until they could tolerate one another, but to create a third thing that had not existed before.<br><br>What was abolished is the law \"of commandments contained in ordinances\" — the regulations that marked the boundary. God's moral will is not repealed here; the wall is.",

    '2:16': "<strong>And that he might reconcile both unto God in one body by the cross</strong> (ἀποκαταλλάξῃ... διὰ τοῦ σταυροῦ)—Reconciliation with God and reconciliation with one another are not two errands. They happen at one cross, in one body.<br><br>Which means a Christianity that is right with God while unreconciled with fellow believers has misread what the cross accomplished. Paul will not let the vertical and the horizontal come apart.",

    '2:17': "<strong>And came and preached peace to you which were afar off, and to them that were nigh</strong>—Christ does not merely make peace and leave its announcement to others. He comes and preaches it; the word that reaches you is his own.<br><br>And the far-off are named first. The gospel's habit is to go to the outsider before congratulating the insider — which is why a church grown comfortable has drifted from it.",

    '2:18': "<strong>For through him we both have access by one Spirit unto the Father</strong> (τὴν προσαγωγὴν)—<em>Prosagōgē</em> was the word for being introduced into a royal presence. You do not present yourself; you are brought in.<br><br>The whole Trinity stands in one short sentence: through the Son, by the Spirit, to the Father. Prayer is not a technique that works but a way that has been opened.",

    '2:19': "<strong>Now therefore ye are no more strangers and foreigners, but fellowcitizens with the saints</strong> (συμπολῖται τῶν ἁγίων)—Not resident aliens admitted on sufferance but citizens, and members of a household. Two images, both about belonging with no conditions attached.<br><br>Paul writes to people whom religion itself had told they stood outside. The gospel does not upgrade their status by degrees; it hands them the family name.",

    '2:20': "<strong>And are built upon the foundation of the apostles and prophets, Jesus Christ himself being the chief corner stone</strong>—The church rests on an apostolic word, not on the piety or consensus of any one generation.<br><br>The <em>akrogōniaios</em>, cornerstone, is the stone that sets the lines for everything after it. Christ does not merely support the building; he determines its shape. No church may square itself by another stone.",

    '2:21': "<strong>In whom all the building fitly framed together groweth unto an holy temple in the Lord</strong> (συναρμολογουμένη)—A building that <em>grows</em> is a deliberate mixing of pictures: masonry and living thing at once.<br><br>The present tense matters for patience. The temple is under construction, which is why it looks unfinished. Impatience with the church — and with oneself — usually assumes a completion Paul has not promised yet.",

    '2:22': "<strong>In whom ye also are builded together for an habitation of God through the Spirit</strong> (συνοικοδομεῖσθε)—Another <em>syn-</em> word: built <em>together</em>. God's dwelling is a joined structure, not a collection of private sanctuaries.<br><br>So the question \"can I not worship God on my own?\" is answered by the architecture. A single stone is not a temple. The Spirit's habitation is the assembled people.",
})

NOTES.update({
    # ---- Chapter 3: the mystery published, and a prayer ----
    '3:1': "<strong>I Paul, the prisoner of Jesus Christ for you Gentiles</strong> (ὁ δέσμιος τοῦ Χριστοῦ Ἰησοῦ)—Paul does not call himself Rome's prisoner, though Rome held the keys. He names the hand he believes is actually holding him.<br><br>This is not denial of the chain but a confession about who governs it. The sentence then breaks off and is not resumed until verse 14 — his circumstances set him digressing into praise rather than complaint.",

    '3:2': "<strong>The dispensation of the grace of God which is given me to you-ward</strong> (τὴν οἰκονομίαν τῆς χάριτος)—<em>Oikonomia</em> is household management: a steward administers what belongs to someone else.<br><br>Paul's ministry is therefore not a possession to defend but a trust to discharge, and its content is <em>grace</em>. A minister with nothing to hand out but requirements has misunderstood the commission.",

    '3:3': "<strong>How that by revelation he made known unto me the mystery</strong> (κατὰ ἀποκάλυψιν ἐγνωρίσθη μοι τὸ μυστήριον)—Paul did not deduce the gospel; it was disclosed to him. The passive verb keeps the initiative with God.<br><br>The same holds for the reader. Nobody reasons their way to the gospel from general principles. It arrives as news, from outside, or it does not arrive at all.",

    '3:4': "<strong>Whereby, when ye read, ye may understand my knowledge in the mystery of Christ</strong>—Paul expects ordinary people, hearing his letter read aloud, to follow him. He is not writing for specialists.<br><br>That expectation shapes how Scripture should be handled. The central matter is plain enough to be read and grasped by the congregation, which is why the text belongs in their hands and not only in the expert's.",

    '3:5': "<strong>Which in other ages was not made known unto the sons of men, as it is now revealed unto his holy apostles and prophets by the Spirit</strong>—The difference between then and now is not that God changed his mind, but that he has spoken.<br><br>Note the \"as it is now.\" Earlier ages were not left in total darkness; they had promise where we have publication. What was once whispered is now announced.",

    '3:7': "<strong>Whereof I was made a minister, according to the gift of the grace of God</strong> (κατὰ τὴν δωρεὰν τῆς χάριτος)—Paul's qualification is twice called a gift. Nothing about his competence, zeal or record is offered as the reason.<br><br>He adds <em>by the effectual working of his power</em>. The ministry is not sustained by the minister's energy either. Both the office and the strength for it are handed over.",

    '3:8': "<strong>Unto me, who am less than the least of all saints, is this grace given</strong> (ἐλαχιστοτέρῳ πάντων ἁγίων)—Paul coins a comparative of a superlative — something like \"leaster than the least\" — as though the language would not go low enough.<br><br>This is not performed modesty. A man who has seen grace clearly stops grading himself against others. The riches he preaches are <em>unsearchable</em>; the preacher is not.",

    '3:9': "<strong>And to make all men see what is the fellowship of the mystery</strong> (φωτίσαι πάντας)—The verb means to bring to light, to illuminate. What was hidden in God is now to be put where anyone can see it.<br><br>\"All men\" is deliberate. The mystery is not reserved for initiates; its whole character is that it has now been published. Keeping it secret would betray it.",

    '3:10': "<strong>That now unto the principalities and powers in heavenly places might be known by the church the manifold wisdom of God</strong> (ἡ πολυποίκιλος σοφία)—<em>Polypoikilos</em> means many-coloured, like embroidery.<br><br>And the display is made <em>by the church</em>. An ordinary congregation of reconciled enemies is God's exhibit before unseen powers. Whatever your church looks like on a wet Sunday, this is what Paul says it is for.",

    '3:11': "<strong>According to the eternal purpose which he purposed in Christ Jesus our Lord</strong> (κατὰ πρόθεσιν τῶν αἰώνων)—None of this was contingency planning. The gathering of the nations was not God's reaction to Israel's failure but his purpose from the first.<br><br>And the purpose is again located <em>in Christ Jesus</em>. Paul will not let God's eternal decisions be discussed anywhere but in the Son, where they can actually be seen.",

    '3:12': "<strong>In whom we have boldness and access with confidence</strong> (παρρησίαν καὶ προσαγωγὴν ἐν πεποιθήσει)—<em>Parrēsia</em> was the freedom of a citizen to speak plainly in the public assembly. Applied to God, it means we need not weigh every word.<br><br>The confidence rests on <em>the faith of him</em>, not on the quality of ours. Approach God boldly and the boldness is borrowed — which is the only kind that holds on a bad day.",

    '3:13': "<strong>Wherefore I desire that ye faint not at my tribulations for you, which is your glory</strong>—Paul, in prison, is anxious about their discouragement rather than his own conditions.<br><br>He calls his suffering <em>your glory</em>. The gospel reached them at a cost someone else paid, as it always does and finally did at the cross. What looks like defeat in the messenger is evidence the message was worth carrying.",

    '3:14': "<strong>For this cause I bow my knees unto the Father of our Lord Jesus Christ</strong>—Paul picks up the sentence he abandoned back in verse 1, and what resumes it is prayer.<br><br>Kneeling was not the usual posture for Jewish prayer; standing was. The detail suggests weight rather than routine. Doctrine that never ends on the knees has been handled as information rather than as news about God.",

    '3:15': "<strong>Of whom the whole family in heaven and earth is named</strong> (πᾶσα πατριὰ ἐν οὐρανοῖς καὶ ἐπὶ γῆς ὀνομάζεται)—There is a play here on <em>patēr</em> and <em>patria</em>: every fatherhood, every family line, takes its name from the Father.<br><br>Human families are therefore the copy, not the original. Whatever your earthly father was or failed to be, he was a likeness — and a poor likeness tells you nothing reliable about the original.",

    '3:16': "<strong>To be strengthened with might by his Spirit in the inner man</strong> (κραταιωθῆναι... εἰς τὸν ἔσω ἄνθρωπον)—The strengthening Paul asks for is interior and largely invisible. He does not pray for relief from their circumstances but for capacity within them.<br><br>And the measure is <em>according to the riches of his glory</em> — not according to whatever we might think reasonable to ask for.",

    '3:17': "<strong>That Christ may dwell in your hearts by faith</strong> (κατοικῆσαι τὸν Χριστὸν... διὰ τῆς πίστεως)—<em>Katoikeō</em> means to settle down and live somewhere, not to visit.<br><br>The means is faith, not feeling. On days when nothing is felt, Christ has not moved out; faith holds what the senses cannot report. <em>Rooted and grounded in love</em> mixes farming with building — both about what lies beneath the surface.",

    '3:18': "<strong>May be able to comprehend with all saints what is the breadth, and length, and depth, and height</strong>—Paul gives four dimensions and names no object for them. The love of Christ, mentioned next, has no measurements to supply.<br><br>Note the <em>with all saints</em>. Even comprehension is corporate here. Nobody takes the measure of Christ's love alone, which is one more reason the Christian life cannot be conducted privately.",

    '3:19': "<strong>And to know the love of Christ, which passeth knowledge</strong> (γνῶναί τε τὴν ὑπερβάλλουσαν τῆς γνώσεως ἀγάπην)—Paul prays that they would know what cannot be known, and the contradiction is deliberate.<br><br>It is the difference between exhausting a subject and being at home in it. You will not reach the bottom of this love; you are meant to live inside it. A God we had fully measured would be too small to be God.",

    '3:20': "<strong>Now unto him that is able to do exceeding abundantly above all that we ask or think</strong> (ὑπὲρ πάντα ποιῆσαι ὑπερεκπερισσοῦ)—Paul piles preposition on preposition, straining after a word large enough for it.<br><br>The limit named is not God's ability but our imagination. And the power concerned is already <em>at work in us</em>, not waiting on better conditions. Prayer that assumes God's reluctance has misread the sentence.",
})
