---
title: "2021 Taxes: Open Source Edition"
layout: post
---

<style>
    table {
        border-collapse: collapse;
    }
    table thead {
        border-bottom: 2px solid #ddd;
        text-align: left;
    }
    table th {
        padding: 10px;
    }
    table td {
        padding: 10px;
        border-top: 1px solid #ddd;
    }

    @media only screen and (min-width: 800px) {
        table {
            margin: 30px;
            width: calc(100% - 60px);
            min-width: 400px;
        }
    }
</style>

Happy Tax Day! The tax industry (by which I primarily mean its largest player,
Intuit) sucks.[^like-really-sucks] As a whole, the industry is an excellent
example of [rent-seeking](https://en.wikipedia.org/wiki/Rent-seeking) behavior,
and not one I wish to encourage with my patronage. So I tried out a few options
when filing my 2021 taxes, and found out a few interesting things along the
way[^including-alternate-communication-methods].

[^including-alternate-communication-methods]:
    One interesting thing I picked up this time around is that the IRS will send
    you alternate forms of communication. Besides the usual standard print
    letters, there's large print and braille, both of which I'd expect, and the
    option to send MP3 files and text/braille files on a USB drive, which I did
    _not_ expect!

    From https://www.irs.gov/forms-pubs/about-form-9000:

    > I elect to receive written communications from the IRS in the following
    > accessible format. Check only one. Forms with more than one box checked will
    > not be processed.
    >
    > - [ ] 00 Standard Print (Cancels prior election)
    > - [ ] 01 Large Print
    > - [ ] 02 Braille
    > - [ ] 03 Audio (MP3)
    > - [ ] 04 Plain Text File (TXT)
    > - [ ] 05 Braille Ready File (BRF)
    >
    > **Note**: You will also receive a standard print copy.

<!--more-->

[^like-really-sucks]: Unless you [work in the tax
    industry](https://www.oxfordreference.com/view/10.1093/acref/9780191826719.001.0001/q-oro-ed4-00010168),
    you probably don't need citations on this one. But there's a ton of
    excellent writing out there!

    From NPR:
    * [Federal Trade Commission accuses Intuit of deceptively advertising TurboTax as free (2022)](https://www.npr.org/2022/03/29/1089490958/free-turbotax-ftc-intuit)
    * [TurboTax Maker Linked To Fight Against 'Return-Free' Tax System (2014)](https://www.npr.org/sections/thetwo-way/2014/04/15/303356915/story-links-turbotax-maker-to-fight-against-return-free-tax-system)
    * [H&R Block, TurboTax Accused Of Obstructing Access To Free Tax Filing (2019)](https://www.npr.org/2019/05/07/720941665/la-city-attorney-sues-intuit-and-h-r-block-alleging-they-undermine-free-tax-fili)
    * [Opposition Blocks Return-Free Tax Filing In U.S. (2013)](https://www.npr.org/2013/03/26/175332655/what-would-the-u-s-be-like-with-no-tax-returns)

    From ProPublica's [Series "The TurboTax Trap"]():
    * [Inside TurboTax’s 20-Year Fight to Stop Americans From Filing Their Taxes for Free (2019)](https://www.propublica.org/article/inside-turbotax-20-year-fight-to-stop-americans-from-filing-their-taxes-for-free)
    * [FTC Sues to Stop “Deceptive” TurboTax “Free” Ad Campaign (2022)](https://www.propublica.org/article/ftc-sues-to-stop-deceptive-turbotax-free-ad-campaign)
    * And [many more excellent articles](https://www.propublica.org/series/the-turbotax-trap)

    Elsewhere:
    * The LA Times: [California tried to save the nation from the misery of tax filing — then Intuit stepped in (2021)](https://www.latimes.com/politics/story/2021-10-21/california-tried-to-save-the-nation-from-the-misery-of-tax-filing-then-intuit-stepped-in)
    * TechCrunch: [TurboTax Maker Funnels Millions To Lobby Against Easier Tax Returns (2013)](https://techcrunch.com/2013/03/27/turbotax-maker-funnels-millions-to-lobby-against-easier-tax-returns/)
    * The Verge: [TurboTax maker lobbies to stop the government from making your returns easier (2013)](https://www.theverge.com/2013/3/26/4150900/intuit-lobbies-against-returns-free-tax-filing-system)
    * [On HN every March-April](https://news.ycombinator.com/item?id=30859747)

!["you took everything from me" meme -- taxpayer: you took everything from me; IRS: I don't even know who you are](taxes/meme.jpg)

{{< toc >}}

## Introduction

In the past, I've fluctuated between filling out paper forms from the IRS and,
more recently, having TurboTax do my taxes for me. This year, I'm tired of
TurboTax's shenanigans, and they no longer (appear to?) participate in the Free
File program, so I'd be paying through the nose for it. In the interest of
finding something better, I tried a few other providers. Also, it's possible
that this will be my last year that I'll fall in the income range where I'll be
eligible for the [Free File program](https://apps.irs.gov/app/freeFile/), so I
figured I'd try out some of the free-as-in-beer software while it's available to
me.

**I <3 open source, so I tried out the two major open-source contenders:**

[**USTaxes.org**](https://ustaxes.org/) is a modern-feeling GPL3-licensed
web/desktop app written with React. It's very usable, though certainly won't
cover every use case for everyone, as its scope is currently fairly limited. I
did my taxes with their web version, but there's a desktop version built with
Tauri, if you want to make extra sure your data never leaves your computer.

[**OpenTaxSolver**](http://opentaxsolver.sourceforge.net/) is a desktop
application, GPL2 licensed, written in C. It exposes a very neat plaintext file
format for managing tax forms, and then uses that data to generate the final
fillable PDFs. However, its
[interface](http://opentaxsolver.sourceforge.net/scrnshot2.html) feels slightly
archaic, as does its ecosystem: Sourceforge, Subversion[^git-svn], and this
[excellent logo](http://opentaxsolver.sourceforge.net/ots3.jpg). However, that's
not a bad thing in my book---the implementation also tends towards Boring (C,
Makefiles, limited dependencies), which is definitely a plus[^compare-to-npm]!

<details>
<summary>More about OpenTaxSolver</summary>

Here's a summary from their website:

> OpenTaxSolver (OTS) is a set of programs and templates for helping you fill
> out your income tax forms.  It performs the tedious arithmetic. OTS is
> intended to assist those who normally prepare their tax forms themselves, and
> who generally know on which lines to enter their numbers. It is meant to be
> used in combination with the instruction booklet corresponding to a given
> form.
>
> This package contains programs and templates for:
> - US-1040 - which also does the Schedules A, B, D, and forms 8949. 
> - Schedule C for US-1040.
> - State Income Taxes for Ohio, New Jersey, Virginia, Pennsylvania,
>   Massachusetts, North Carolina, and California taxes updated for the 2021
>   Tax-Year.
>
> Also contains an Automatic PDF Form-Fillout function:
> - Supports all Federal Forms and State Forms. Saves time by filling out many
>   of the numbers. You may still need to enter some information or check boxes
>   that are not handled by OTS. Tested to work properly with many PDF viewers.
> - You can edit your forms with Libre-Office.

[^git-svn]: Compiling the source for OpenTaxSolver did give me my first
    introduction into `git-svn`, which is pretty great!

    ```sh
    git svn clone https://svn.code.sf.net/p/opentaxsolver/SrcCodeRepo/ opentaxsolver
    ```

[^compare-to-npm]: 
    ```text
    % du -hs opentaxsolver/trunk/*
    1016K	opentaxsolver/trunk/OTS_2017
    7.2M	opentaxsolver/trunk/OTS_2018
    6.9M	opentaxsolver/trunk/OTS_2019
    7.0M	opentaxsolver/trunk/OTS_2020
    9.0M	opentaxsolver/trunk/OTS_2021
    ```

    Compare this to USTaxes.org's software, written in Javascript:
    ```text
    % du -hs node_modules
    656M	node_modules
    % find node_modules | wc -l
    93728
    ```

    Plus Rust stuff, for Tauri, not known for its compile speed.

    Building OpenTaxSolver didn't make me install or download anything except
    the `gcc`/`make` toolchain, and `gtk+-2.0`, all of which I already had
    installed, and occupies more than an order of magnitude less disk space.

Here's an architecture diagram from their website:
![opentaxsolver architecture](taxes/opentaxsolver/architecture.gif)

Their file format is really interesting. Here's a snippet from my file from this
year:

```txt
Title:  US Federal 1040 Tax Form - 2021

 { --- Your Filing Status & Exemptions --- }
Status	Single	 { Single, Married/Joint, Head_of_House, Married/Sep, Widow(er) }
You_65+Over?	N	 { Were you born before January 2, 1957 ? (answer: Yes, No) }
You_Blind?	N	 { Are you blind ? (answer: Yes, No) }
Spouse_65+Over?	N	 { Was Spouse born before January 2, 1957 ? (answer: Yes, No) }
Spouse_Blind?	N	 { Is Spouse blind ? (answer: Yes, No) }
Dependents	1	 { Number of Dependents, (answer: 1, 2, 3, 4, 5, 6, 7, 8, 9, ...)
				self=1, spouse, etc. }
VirtCurr?	N	 { During 2021, did you buy/sell/exchange/trade any Virtual Currency ? (answer: Yes, No) }
 { ---- Income ---- }
 { -- Wages, salaries, tips (W-2's Box-1). -- }
L1	12345.67	
		;
 { --- Interest --- }
 { -- Tax-Exempt Interest. (Only used for SocialSecurity calculations). --
      (Any private activity bond interest exempt from regular tax, is entered under Schedule 2 below.) }
L2a			;
 { -- Taxable Interest -- 1099-INT(s) box 1 }
L2b	20.13	
		
		;
 { --- Dividends --- }
 { -- Qualified Dividends 1099-DIV box 1b -- }
L3a	72.97	
		;
 { -- Ordinary Dividends 1099-DIV box 1a. -- }
L3b	120.95	
		;
 { --- Other Income & Credits --- }
L4a			; { IRA distributions. }
L4b			; { Taxable IRA distributions. }
L5a			; { Pensions, Annuites. }
L5b			; { Taxable Pensions, Annuites. }
L6a			; { Social Security benefits.  Forms SSA-1099 box-5. }
CharityCC	200		; { Charity contributions by Cash or Check. }
CharityOT			; { Charity contributions Other Than cash or check. }
CharityCO			; { Charity contributions CarryOver from prior year. }
L13			; { Qualified business income deduction. }
L19			; { Child tax credit/credit for other dependents. }
L25a	1234.56		; { Federal income tax withheld, from W-2's, box-2. }
L25b			; { Federal income tax withheld, from 1099's. }
L25c			; { Federal income tax withheld, from other forms. }
L26			; { Estimated tax payments made for the year. }
```

</details>

**As a control group, I compared the results with several other providers:**

[**TurboTax**](https://turbotax.intuit.com/) may be Satan incarnate, but I
wanted to include it for completeness' sake.

[**FreeTaxUSA.com**](https://www.freetaxusa.com/) is a frequently recommended
competitor to TurboTax.

[**OLT.com**](https://www.olt.com/) was the only Free File provider that would
also file my state returns for free.

**Not under consideration this time around:**

**Filling out forms myself**: While doing my taxes five consecutive times gave
me a pretty good overview of what I'd need to do, I wasn't prepared to attempt
doing my taxes unassisted this year. Perhaps next year, since I should be able
to mostly copy/paste from my 2021 tax return.

[**Free File Fillable Forms**](https://www.irs.gov/e-file-providers/free-file-fillable-forms)
https://www.freefilefillableforms.com/home/default.php

**A paid tax preparer** like H&R Block (which I've heard is the TurboTax of
in-person tax preparers) or your local CPA. This option tends to be
prohibitively expensive, and won't likely end up saving me much time.


## Getting started

### UsTaxes.org

Perhaps unsurprisingly, the open-source version was the easiest to sign up for,
in that no signup whatsoever is required. (This _does_ mean that they may lose
your data if you start a return and don't complete it. It wasn't entirely clear
to me how the data was stored---[localStorage mostly, I
think?](https://github.com/ustaxes/UsTaxes/blob/master/src/redux/store.ts#L11)---but
I avoided refreshing the page just in case.) Just visit their website and go!

Otherwise, you can download their desktop app and run locally:

https://github.com/ustaxes/UsTaxes/releases

Selecting and downloading an appropriate executable for one's platform is
perhaps the least user-friendly part of the process. The download takes you
straight to GitHub releases, with no indication of whether you want the `.msi`
(Windows), the `.dmg` (MacOS), the `.deb` (Debian/Ubuntu/Mint/...), the
`.AppImage`, .... While I might feel comfortable recommending UsTaxes.org to my
parents from a general usability standpoint, I wouldn't expect them to
necessarily figure out GitHub Releases just to install the software.


### OpenTaxSolver
Download OpenTaxSolver from
http://opentaxsolver.sourceforge.net/download2021.html, extract and run:

```sh
tar xf OpenTaxSolver2021_19.07_linux64.tgz
cd OpenTaxSolver2021_19.07_linux64
./Run_taxsolve_GUI
```

Documentation is available online: http://opentaxsolver.sourceforge.net/usage.html

There are prebuilt versions, and some distros have it packaged. Still, not ready
for non-nerds.

### Paid providers

All three required me to sign up for an account, but there was nothing
noteworthy about the process for any of them. Except FreeTaxUSA, which is
convinced that usernames are secrets? (Shh, don't tell anyone!)

![Don't share your username, kids!](taxes/freetaxusa/username-is-secret.png)

Each suggests, with varying degrees of intensity, that I add a phone number to
"secure my account"---presumably with SMS-based 2fa. I didn't dig around in any
menus to figure out if they supported TOTP or not. I get enough SMS spam as it
is, so I declined giving any of the three my phone number. Based on the number
of promotional emails I've gotten this week from Intuit, this may have been
wise.

Oh, and TurboTax wants to get its hands on all the information it can:

![turbotax asks for consent to use user data for slightly nebulous reasons](taxes/turbotax/intuit-wants-to-use-your-return-info.png)

## Pricing

The open-source options are, unsurprisingly, free of cost.

### TurboTax

TurboTax provides a questionnaire that helpfully slots you into one of their
product ranges. ("Expert help as you go" ("Get unlimited help from tax experts
and a review before you file.") and "We do your taxes for you" ("A tax expert
will prepare, sign, and file your taxes for you.") are a substantial additional
cost.)

I was immediately put off to discover that their pricing is different whether or
not you've already created an account. (I have notes that they also had a
$69[^nice] Deluxe price listed somewhere, but was unable to find that. Might be
an error on my part, or that I wasn't able to reproduce the set of conditions
for which they quote that particular price point.) Note the difference in the
Premier and Self-Employed price tiers:

[^nice]: Nice.

![turbotax pricing without an account](taxes/turbotax/turbotax-pricing-2.png)

Without an account:

![turbotax pricing with an account](taxes/turbotax/turbotax-pricing-1.png)

These prices, too, are pretty deceptive; they fairly clearly advertise the cost
as the federal cost---and oh, by the way, it's $50 extra to file your state
taxes too. (I suppose this _is_ reasonable in states that don't have a state
income tax, like Washington, Florida, and Texas; those states will just pay the
quoted base fee.) After seeing this, I'd expect to pay $59, but the real cost is
$108 once you add the $49 state filing fee on:

![pricing banner ignoring state tax fees](taxes/turbotax/intuit-pricing-banner.png)

They do have a free offering, but it's pretty limited. From Intuit's website:
> A simple tax return is Form 1040 only.
>
> Situations covered in TurboTax Free Edition include:
>  * W-2 income
>  * Limited interest and dividend income reported on a 1099-INT or 1099-DIV
>  * Claiming the standard deduction
>  * Earned Income Tax Credit (EIC)
>  * Child tax credits
>  * Student Loan Interest deduction
>
> Situations not covered in TurboTax Free Edition include:
>
>  * Itemized deductions
>  * Unemployment income reported on a 1099-G
>  * Business or 1099-NEC income
>  * Stock sales
>  * Rental property income
>  * Credits, deductions and income reported on schedules 1-3

Since I participated in Pearson's Employee Stock Purchase Program, I would have
needed to pay for the $89 Federal/$49 State/maybe additional hidden fees? for
Premier:

![turbotax upsell 1](taxes/turbotax/upgrade-nag-1.png)

### FreeTaxUSA

FreeTaxUSA, as the name implies, allows you to fill out your federal returns for
free, and charges $15 for your state return.

They [participate in the Free File
program](https://www.freetaxusa.com/freefile2021/), but only up to an AGI of
$41,000, and they do make that page rather difficult to find---it's not linked
to from their home page at all.

### OLT.com

OLT.com offers free federal and state tax returns up to a $73k AGI cap. Above
that, it's $9.95. They also have a $7.95 premium edition that offers phone/chat
support and audit support.

### Pricing Summary

I really don't understand why Intuit draws a 5-10x premium over the other
providers. Their service is somewhere between somewhat better and slightly worse
depending on which metric you go by; certainly not 5-10x better!

| Service       | Cost (federal) | Cost (state) | Cost (if eligible for Free File) | Free File AGI Cap  |
|---------------|----------------|--------------|----------------------------------|--------------------|
| UsTaxes.org   | $0             | $0           | $0                               | N/A                |
| OpenTaxSolver | $0             | $0           | $0                               | N/A                |
| TurboTax      | $0-$300+       | $49.99+      | N/A                              | No Free File Offer |
| FreeTaxUSA    | $0             | $14.99       | $0                               | $41k               |
| OLT.com       | $0             | $9.95        | $0                               | $73k               |

## Results Summary

Turns out, especially for fairly straightforward returns like mine, most
services do a pretty comparable job. Each paid service got me the same return
on each form to the dollar. OpenTaxSolver got me the same federal return after
a few attempts, and UsTaxes.org offered me a $47 lower refund thanks to not
supporting deductions for line 12a.

| Service       | Federal return | State Return | M1PR |
|---------------|----------------|--------------|------|
| UsTaxes.org   | $(X-47)        | N/A          | N/A  |
| OpenTaxSolver | $X             | N/A          | N/A  |
| TurboTax      | $X             | $Y           | $Z   |
| FreeTaxUSA    | $X             | $Y           | $Z   |
| OLT.com       | $X             | $Y           | $Z   |

(Dollar values omitted for privacy reasons.)


## User Experience

### UsTaxes.org

Definitely the best UI, narrowly edging out TurboTax. They use Material UI,
which feels very familiar to me, and have clearly put thought into things like
tab indexing, so navigating around feels very natural. I didn't try filling it
out on a mobile device (I'm not _that_ much of a masochist), but their mobile UI
seems very passable as well.

There's very little friction to getting started: No account to create, no terms
of service or privacy policy to agree to, no application to install; just visit
the website and get started.

Also, I noticed it was a bit quicker to run through my forms too. Many of the
other services had me copying over data from _every box_ of every form I
received, but UsTaxes.org seemed to only have me extract the relevant bits.

There's an [open issue](https://github.com/ustaxes/UsTaxes/issues/1110) tracking
progress on allowing federal return submission through FreeFileFillableForms,
but otherwise UsTaxes.org expects you to print out and mail in your forms, which
isn't nearly as convenient as e-filing.

### OpenTaxSolver

OpenTaxSolver was the only piece of software with which I made mistakes -- and I
did it last, so I knew what I was looking for. I had to go back twice and
correct values I'd omitted or misplaced. Unfortunately, this does just speak to
the confusing interface of OpenTaxSolver. As its website says, it's definitely
targeted at people who have a high degree of familiarity with the forms it's
filling out for you, though at that point I'm not sure why I wouldn't want to
just fill out forms myself.

Here's one place I messed up: I received a 1099-B from Pearson's employee
stock purchase plan. The 1099-B, and every other software, refers to these
fields, among others:

 * Description
 * Date acquired
 * Date sold
 * Proceeds
 * Cost or other basis
 * Type of gain/loss (short or long term)

Here's OpenTaxSolver's interpretation of those fields:

![opentaxsolver capital gains fields](taxes/opentaxsolver/capital-gains-ui.png)

I have no doubt that if I had to file my taxes weekly or even monthly, I'd be
using OpenTaxSolver. However, I'm not prepared to learn a domain-specific
language (even if it's super cool!) for a set of forms I have to fill out once
annually.

[![xkcd 1205 "Is it worth the time?"](taxes/is_it_worth_the_time.png)](https://xkcd.com/1205/)

OpenTaxSolver expects you to print and mail your tax returns.

### OLT.com

Form fields are a little bit odd. Certain elements edit hyphens and such in with
JavaScript. The phone number fields are all formatted as two fields; one for the
area code, and another for the exchange and subscriber number (so a number like
`(320) 555-1212` would be represented in two fields: `[ 320 ][ 5551212 ]`),
which led to me reliably either typing all ten digits of phone numbers into the
area code box, or hitting tab again after the exchange code (`555` in this
example). The tab order for addresses is "Address Line", "ZIP Code", "City",
"State", which often leads me to begin typing the city in the ZIP field. (This
is sort of reasonable, though, since they do attempt to auto-fill the city and
state from the ZIP Code.)

I mistakenly clicked to add a form which I didn't have. The site wouldn't allow
me to move on from that page until I'd filled out the title and the TIN, which,
of course, I didn't have! It _did_ let me log out and log back in, which
apparently reset the session sufficiently to allow me to continue.

### FreeTaxUSA

Pleasant to use. Not over-the-top fancy like TurboTax, nor as barebones as OLT.
I got a single attempt to upsell during the process, and likely would have had
one or two more if I attempted to file with them. (However, I find a $7 Deluxe
package a lot less offensive than the several-hundred-dollar upgrades that
Intuit tries to push!)

![freetaxusa upsell interstitial](taxes/freetaxusa/interstitial.png)

### TurboTax

Prompts me to enter a phone number (skippable, but not obvious) every time I log
in.

Spams me with email after signing up. <!-- TODO: verify? even after attempting
to unsubscribe:--> It's possible I'm a dummy, and somehow clicked something to
sign me up for Mint, but I never intentionally navigated to Mint, so these
emails are just all unsolicited Intuit spam:

![a mailbox full of intuit spam](taxes/turbotax/spam.png)

Auto-import is...almost nice? Except I have to enter employer TIN, Box 1 of my
W-2, and the box d ("Control number") of my W-2, and then proofread---at this
point, I might as well just fill in all the information myself! I don't consider
this much of a benefit at all; I don't really think it saved me any time, though
it was able to import the majority of the information I needed.

The number of animations, interstitials, and aggressive upgrade prompts I had to
sit/click through really tested my patience. It's incredible they're leading the
market with such a user-hostile product.

![turbotax upsell 2](taxes/turbotax/upgrade-nag-2.png)
![turbotax upsell 3](taxes/turbotax/upgrade-nag-3.png)

## How much legal gunk I had to read to use each service

| Service       | `cat privacy_policy terms_of_use \| wc` (lines, words, characters) |
|---------------|-----------------------------------------|
| UsTaxes.org   | 0                                       |
| OpenTaxSolver | 0                                       |
| TurboTax      | `1006   24328  155006`                  |
| FreeTaxUSA    | `183    6901   43255`                   |
| OLT.com       | `323    8250   52270`                   |
| [Franz Kafka's Metamorphosis](https://gutenberg.org/ebooks/5200) (for scale) | `2266   25094  142017` |

So TurboTax's privacy policy and terms of use is both longer and more boring
than Kafka's _Metamorphosis_. Hmm.

## So, is open-source tax software ready?

Honestly, as much as I'd like to say otherwise, **no, it's not.** If your tax
situation is exceptionally simple, then you can use UsTaxes.org---but
TurboTax's free product should cover most of those cases too, and will allow you
to e-file. If you're eligible for Free File, either OLT.com or FreeTaxUSA is
perfectly fine.

If you have a lot of patience and interest in _understanding_ what you're
doing, you can use OpenTaxSolver---but you can also fill in the forms yourself,
and again, FreeFileFillableForms will allow you to e-submit here.

The great thing about open source software is that I can contribute! I've been
working on some PRs to UsTaxes.org (which unfortunately didn't make it in before
tax day, but may help late filers), and I've been playing around with getting
Minnesota's state returns supported. Hopefully, in another year or two, it will
be in a state where I'll feel comfortable recommending it to everyone. And, of
course, the sooner TurboTax dies a flaming death, the happier I'll be!
