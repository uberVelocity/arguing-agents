import re
import requests

from sys import argv

def retrieveArguments(url, isPro):
    print(url)
    if isPro:
        arg_type = "pro"
    else:
        arg_type = "con"

    if 'answers' in url:
        regex = '<div class="newblue-' + arg_type + '-quote-box">(.*?)</div>\n<br />\n<br />\n</div><br />'
    elif 'resource' in url:
        regex = '<td id="newblue-' + arg_type + '.*?>\n<div class="newblue-top-' + arg_type + '-quote-box">(.*?)</td>'
    else:
        regex = '<blockquote .*?argument-type-' + arg_type + '.*?>(.*?)</blockquote>'

    string = requests.get(url).text
    #<blockquote class="argument-box argument-type-pro dotdotdot cf-tweet-this cf-tt-target cf-tt-element-attached-center cf-tt-target-attached-center cf-tt-enabled cf-tt-abutted cf-tt-abutted-top cf-tt-element-attached-bottom cf-tt-target-attached-top cf-tt-out-of-bounds cf-tt-out-of-bounds-top" id="argument-41" style=""><h3>Pro 1</h3>
#<h4>The Second Amendment is not an unlimited right to own guns.</h4>
#In the June 26, 2008 <span style="font-style: italic">District of Columbia et al. v. Heller</span> US Supreme Court majority opinion, Justice Antonin Scalia, LLB, wrote, "Like most rights, the right secured by the Second Amendment is not unlimited… nothing in our opinion should be taken to cast doubt on longstanding prohibitions on the possession of firearms by felons and the mentally ill, or laws forbidding the carrying of firearms in sensitive places such as schools and government buildings, or laws imposing conditions and qualifications on the commercial sale of arms." <span class="footnotes-link">[<a href="/additional-resources/footnotes-sources/#3">3</a>]</span> On June 9, 2016 the US Ninth Circuit Court of Appeals ruled 7-4 that "[t]he right of the general public to carry a concealed firearm in public is not, and never has been, protected by the Second Amendment," thus upholding a law requiring a permitting process and "good cause" for concealed carry licenses in California. <span class="footnotes-link">[<a href="/additional-resources/footnotes-sources/#145">145</a>]</span><span class="footnotes-link">[<a href="/additional-resources/footnotes-sources/#146">146</a>]</span> A 2018 study found that 91% of the 1,153 court cases with claims stating a government action or law violates the Second Amendment between the 2008 <span style="font-style: italic">DC v. Heller</span> decision and Feb. 1, 2016 failed. <span class="footnotes-link">[<a href="/additional-resources/footnotes-sources/#157">157</a>]</span> <a class="open-popup-link dotdotdot-exempt ddd-keep" onclick="__gaTracker('send','event','tiles-arguments','-click','tile-01-pro-read-more')" href="#argument-41-popup">Read More</a></blockquote>
    #arguments = re.findall('<blockquote .*?argument-type-' + arg_type + '.*?>(.*?)</blockquote>', string, flags=re.DOTALL)
    #arguments = re.findall('<div class="newblue-' + arg_type + '-quote-box">(.*?)</div>\n<br />\n<br />\n</div><br />', string, flags=re.DOTALL)
    arguments = re.findall(regex, string, flags=re.DOTALL)

    return arguments

def retrievePros(url):
    return retrieveArguments(url, True)

def retrieveCons(url):
    return retrieveArguments(url, False)

url = 'https://medicalmarijuana.procon.org/view.answers.php?questionID=001325'
url = 'https://gun-control.procon.org/'

pros = retrieveCons(argv[1])

for pro in pros:
    print("___Argument___\n", pro, "\n")