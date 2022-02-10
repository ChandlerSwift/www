---
title: How not to send an email asking for personal information
layout: post
IncludeSyntaxStyles: yes
---

May-July 2017: [Equifax is hacked](https://en.wikipedia.org/wiki/2017_Equifax_data_breach).
September 7, 2017: Equifax discloses the breach.
July 24?, 2019: I make a claim against the settlement fund, since my information
    was involved in the breach.
January 27, 2022: I receive an email from the Equifax Breach Settlement
    Administrator telling me how I can claim the credit monitoring I selected.
January 30, 2022: I spend several hours trying unsuccessfully to decide if the
    email is legitimate or not.

<!--more-->

As a professional in a computer-related field, I spend a lot of time fielding
computer-related questions, and trying to help friends and family understand how
to safely use technology. It's a constant struggle---there are a lot of scams
out there, and new ones popping up all the time. I have a few pieces of fairly
general advice I tend to hand out for people looking to see if an email they've
received is legitimate or not, summarized here:

 * Check if the domain is known to be trusted[^domains]. For example, a password
   reset email from noreply@google.com may be safe, but an email from
   noreply@google.account-service.info is almost certainly out to get you.
 * Check if the links lead where you expect. If I have an email with the FROM
   header[^which-is-spoofable] as noreply@accounts.google.com, but all the links
   lead to http://555.867.530.900/... (a personal favorite "IP address"---big
   scare quotes here---that Pearson gave as part of an internal phishing
   awareness training; spot the
   [Tommy Tutone reference](https://www.youtube.com/watch?v=6WTdTwcmxyo)!), then
   it's a malicious link.
 * If you see something you're not suspecting, or your gut tells you something
   is suspicious, it probably is. Make sure to validate anything you're being
   sent, usually by looking it up on the website that the email claims to be
   from. ("Call the number on the back of your card" is a good example of this.)
   Or check in with an expert! I encourage my friends and family to forward me
   anything they're unsure about, if they want a second opinion on if it's legit
   or not.
 * And, of course, have caution proportionate to the risk. I'm less concerned
   about losing my Spotify password than I am my bank's password, and it would
   be a red flag if a link claiming to be from Spotify started asking me about
   my bank info.

The email I received telling me how to claim my credit monitoring is...terrible.
It violates every single principle in the list above, to such a comical degree
that I felt compelled to write it up. If you need to send out an email, just do
the opposite of what they did, and you'll probably be good! Let's see how they
violate every single point I've laid out above:

<style>blockquote p { margin: 0; }</style>

### Check if the domain is known to be trusted.

An email from Equifax should come from equifax.com or a subdomain. Well, I
guess this isn't from _Equifax_, it's from some law firm or something. Okay,
a quick Google search says equifaxbreachsettlement is right. (And, as a person
who loves using the view-source button, I can also verify that SPF, DMARC, and
DKIM all pass, but this took me a while to remember how to do (it's just in the
headers), and wouldn't be something I'd expect most people to check.)
```text
Authentication-Results: aspmx1.migadu.com;
	dkim=pass header.d=equifaxbreachsettlement.com header.s=smtp header.b=SqYR676H;
	dmarc=pass (policy=quarantine) header.from=equifaxbreachsettlement.com;
	spf=pass (aspmx1.migadu.com: domain of "bounce+17882d.ae1aa8-chandler=chandlerswift.com@equifaxbreachsettlement.com" designates 69.72.40.1 as permitted sender) smtp.mailfrom="bounce+17882d.ae1aa8-chandler=chandlerswift.com@equifaxbreachsettlement.com"
```

### Check if the links lead where you expect.

equifaxidworks.com is the type of domain I'd register if I were trying to phish
Equifax customers. I can't get equifax.com, of course, but I can tack some other
words onto the end, and call that my site. My current leading contender is
experianidentityprotection.com, which is available for <$9 at the time of
writing, but any number of others would be equally convincing. 

```html
  <td>Visit the Experian IdentityWorks Website:=20
  <a href=3D"https://email.equifaxbreachsettlement.com/c/eJxFjk2PgjAURX8NLE=
n7-CgsuiCKExbiRF3Mjjza19CI6JRO6s8fJmomuYub3OScqyUSRyxjK4EBMA6CCyagSrggbVLNO=
ZKpMj1EGaPvH2vwMThCNS7k_URXmn2ibtd4lIpXxVAwQMQsL_M8LZVJixIyMMSFwniSo_f3JUrr=
CHZrQggJPe7kLM5Wh5u7LH-odXmJ_hWxk2rEWU_k1h_vugRrnnYvm91Xvzk22_a8P3Tt-XDsN_X=
-s24_uv7UdNu--gX9ZUxy">www.experianidworks.com/equifaxsettlement</a></td>
```

Oh, and that's just the text of the link---the actual link doesn't lead there.
They've obscured the actual link behind a tracking redirect, so even the
location I already thought was suspicious isn't what I see. Nice.

### If something is suspicious...

Well, it kinda ticks all the boxes: "claim your free ______", "time limited", "click here", "enter
all your personal information, including DOB and SSN"...

### Validate information on the website the email claims to be from.

In this case, the email is from equifaxbreachsettlement.com, so their website
should have some note that they're currently sending out these emails, and that
you'll be able to claim your credit monitoring at experianidworks.com in the
email they'll send. But https://www.equifaxbreachsettlement.com mentions
experianidworks.com...exactly zero times. Not once! The closest they come is in
the FAQ, where they say

> **I received an email regarding free, three-bureau (Equifax, Experian, and
> TransUnion) credit monitoring from Experian for four years. Is this email
> legitimate?**
>
> If you made a valid claim for Credit Monitoring Services, you will receive an
> email from the Equifax Data Breach Settlement Administrator (from the email
> address info@equifaxbreachsettlement.com) by February 25, 2022 providing you
> with information on how to activate your credit monitoring. The Settlement
> Administrator will provide you with an activation code and link to the
> Experian website where you can enroll and activate your Credit Monitoring
> Services.

But none of that would prevent an enterprising scammer from realizing that these
are emails going out, and sending out their own emails using the same template,
that link to another service. (As mentioned above, experianidprotection.com is
available for $9, and looks no less trustworthy than experianidworks.com!)

Well, if equifaxbreachsettlement.com doesn't give me any information, let's see
if Experian links there? Not that I can find. They do have a product called
"[Experian IdentityWorks&trade;](https://www.experian.com/consumer-products/identity-theft-and-credit-protection.html)"
but that entire registration flow happens on the experian.com domain, as I'd
have expected.

How about a quick web search? Well, all the results for "experian id works" and
a few other related search queries either just return links to the
experianidworks.com page, or to similarly named pages on the experian.com domain
that experianidworks.com seems to be a clone of, or reviews/articles talking
about Experian's credit monitoring program (again, named IdentityWorks, but all
on the experian.com domain, bolstering my suspicion that this could just be a
domain impersonating Experian).

<div style="max-height: 40em; overflow-y: scroll;">
<img style="margin: 0; padding: 0; max-width: 100%;" src="/images/experian-id-works-search.png" alt="search results for “experian id works”" title="This is DuckDuckGo, but Google's results are similar; I checked!">
</div>

Hm. Let's try the command line, and make sure that Experian is actually the one
to have registered the domain:
```text
% whois experian.com
[...]
Domain Name: EXPERIAN.COM
Registry Domain ID: 5503875_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.networksolutions.com
Registrar URL: http://networksolutions.com
Updated Date: 2021-08-30T16:21:45Z
Creation Date: 1996-10-28T05:00:00Z
Registrar Registration Expiration Date: 2022-10-27T04:00:00Z
Registrar: Network Solutions, LLC
Registrar IANA ID: 2
Reseller: 
Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
Registry Registrant ID: 
Registrant Name: Information Solutions, Experian
Registrant Organization: Experian Information Solutions, Inc.
Registrant Street: 475 ANTON BLVD
Registrant City: COSTA MESA
Registrant State/Province: CA
Registrant Postal Code: 92626-7037
Registrant Country: US
Registrant Phone: +1.7148307000
Registrant Phone Ext: 
Registrant Fax: 
Registrant Fax Ext: 
Registrant Email: domainadmin@experian.com
[...]
% whois experianidworks.com
[...]
Domain Name: experianidworks.com
Registry Domain ID: 1978500106_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.corporatedomains.com
Registrar URL: www.cscprotectsbrands.com
Updated Date: 2021-11-07T01:04:51Z
Creation Date: 2015-11-11T13:43:29Z
Registrar Registration Expiration Date: 2022-11-11T18:43:29Z
Registrar: CSC CORPORATE DOMAINS, INC.
Sponsoring Registrar IANA ID: 299
Registrar Abuse Contact Email: domainabuse@cscglobal.com
Registrar Abuse Contact Phone: +1.8887802723
Domain Status: clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited
Registry Registrant ID: 
Registrant Name: Domain Management
Registrant Organization: Consumerinfo.com, Inc.
Registrant Street: 535 Anton Blvd, Suite 100
Registrant City: Costa Mesa
Registrant State/Province: CA
Registrant Postal Code: 92626
Registrant Country: US
Registrant Phone: +1.8003570821
Registrant Phone Ext: 
Registrant Fax: +1.8003570821
Registrant Fax Ext: 
Registrant Email: DNSAdmin@consumerinfo.com
[...]
```

So they're not registered by the same organization...or even the same registrar!
There's no link on equifaxbreachsettlement.com or experian.com to this site;
it's registered by and through a different organization than the base Experian
domain; it's on a domain that _looks_ like it's intended to be deceptive...there
are a lot of reasons not to trust this domain at this point.

### Have caution proportionate to the risk.

Well, it may be sketchy, but at least they ask for all my personal information,
including my full name, email address, mailing address, date of birth, and some
common security questions and answers!

### Oh, and news organizations are somewhere between useless and actively harmful.
Perhaps unsurprisingly, I'm not the only one to be asking whether this is
legitimate, so there are a decent number of answers out there.

Snopes has a decent answer, but they sort of hide any nuance behind an "is this
email legit" question and a big green "Yes!" at the top, which doesn't really
encourage people to appreciate that it's not necessarily a yes/no question; but
that there's a bit more subtlety behind it.

Another of the top links on a web search for "experianidworks", at the time of
writing, was
https://www.10news.com/news/fact-or-fiction/fact-or-fiction-equifax-settlement-email-is-legit,
which has the following advice:

> We're clearing up some confusion over an email you may have received.
>
> The email appears to concern a settlement over the 2017 Equifax data breach.
>
> It offers you 4 free years of the credit monitoring service Experian Identity
> Works.
>
> The body of the email contains a link to Experian's site in which you have to
> provide a lot of personal information.
>
> But don't worry, it's legit.

This is, in my opinion, exceptionally bad advice, given without qualification.
(Remember, [only a Sith deals in absolutes](https://knowyourmeme.com/memes/only-a-sith-deals-in-absolutes)!)
A more nuanced take might look something like

> That link should lead to experianidworks.com. If it does, _then_ it's legit.

As usual, [Reddit does a much better job](https://www.reddit.com/r/Scams/comments/sewb78/equifax_breach_settlement_email_legit/hv07z46/).
Here's [u/lunarchuck](https://www.reddit.com/user/lunarchuck):

> I received the email yesterday at my gmail address. Whois lookup on
> experianidworks.com produces a registration address (535 Anton Blvd, Suite
> 100, Costa Mesa, CA, 92626, US) that appears to be associated with Experian
> per BBB. Googling the domain brings up a bunch of legitimate sources that link
> to it (universities, state governments).
>
> Gmail headers show that the sending domain equifaxbreachsettlement.com passes
> dkim and dmarc and the sending ip address passes SPF for that domain. And that
> domain is linked from the FTC site.
>
> I think it's legit. It would have to be one of the all-time greatest
> phishing/hacking scams to not be, especially since it's been out there for at
> least 3 days.

That is, "Given this domain, here's what I checked. It all checks out; here's
how to reproduce my results; and despite checking, I'm still not going to claim
it's absolutely safe, so you should still use appropriate caution"---exactly
what I'd have wanted from any other analysis.

### So it's legit?

Yeah, I think so. Despite the total lack of effort of anyone involved to help
reassure me that it's legit, I've filled in my information and feel relatively
comfortable having done so. Plus, in the time between when I received this email
and did the original checking, and when I wrote the post, there's a lot of new,
better information out there.

The clincher, for me, which should have been plastered all over the place, is
a link to the [FTC's Equifax settlement page](https://www.ftc.gov/enforcement/cases-proceedings/refunds/equifax-data-breach-settlement),
which mentions both info@equifaxbreachsettlement.com as the email source and
https://www.experianidworks.com/equifaxsettlement as the link's target.

That said, for a settlement regarding poor security practice by a company that
_definitely should have known better_, this is embarrassing! They fail every
single heuristic I'd use to verify that this is legit. And, perhaps more
importantly, they're working against the community of security professionals who
try to educate people on good security practice. Do better!

[^domains]: One issue I'm glossing over here is that to a person who hasn't
    spent a _lot_ of time around computers, it's certainly non-obvious which
    bits of a URL are important and which aren't. I trust google.com/\*, and
    account-info.google.com/* (or I would, if I didn't happen to know that
    Google uses accounts.google.com for account-related pages), but I definitely
    wouldn't trust google.account-info.com. And watch out for the particularly
    devious ones like accounts.google.com-helpandsupport.tk/...! The thing that
    makes this especially difficult is that I can't simply say to look at the
    beginning of the URL, because that's just a subdomain. I can't say to look
    at the end, because that's not the host. I have to explain to look for the
    first slash after https://, and then look at whatever's one (or two, in
    cases like *.gov.uk) dot-separated chunk before that. Or suggest to read
    [MDN's "What is a URL?"](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL#basics_anatomy_of_a_url)[^the-m-in-mdn-should-stand-for-marvelous]---or,
    perhaps, read
    [any](https://datatracker.ietf.org/doc/html/rfc1034/)
    [of](https://datatracker.ietf.org/doc/html/rfc1630/)
    [the](https://datatracker.ietf.org/doc/html/rfc2616/#section-3.2.2)
    [relevant](https://datatracker.ietf.org/doc/html/rfc3986/)
    [RFCs](https://datatracker.ietf.org/doc/html/rfc3987/) (or better yet, the
    [Living Spec on URLs](https://url.spec.whatwg.org/))? Riiiiiight, I'm trying
    to save people the hassle of needing a degree in networking to not leak
    their bank password!

    This is one reason I'm generally not opposed to browsers drastically
    reducing the amount of information they display in the URL bar: It's a pain
    for people who _do_ want all that information, but for most people, the
    query string isn't information they care about.

[^the-m-in-mdn-should-stand-for-marvelous]: Despite my tone in the rest of that
    paragraph, I'm a huge fan of that document. MDN does a surprisingly
    excellent job of explaining these concepts in an approachable way. Despite
    the technical nature of the topic, I think I would feel comfortable sending
    my mother this document if I thought she really needed to know a bit more
    about the nitty-gritty of URL structure than she currently does.

[^which-is-spoofable]: As a reminder, the FROM line in an email is just text,
    and I can set it to whatever I want (though this is getting better! SPF,
    DKIM, and DMARC are all strides in the right direction).
    [Eric](https://ericvillnow.com) and I had a fun time in high school spoofing
    emails from school administration to our friends, which somehow didn't turn
    out poorly for anyone involved.
