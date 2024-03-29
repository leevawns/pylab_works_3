"""
Hello,

For those of you that
- want to surf on the edge of Web technology without understanding it,
- desire to be considered as a software guru,
- are forced to write technical documents that nobody will read.
- want to laugh a bit,

I have written a "Bullshit Generator" script in Python (see below). It
generates English sentences at random, talking about leading-edge Web-based
technologies. For example it can produce simple sentences like

"The interface subscriber manages the web-based online ontology."

or more complex, like

"Generally speaking, the architecture is collected by the client from the
encapsulation related to the artifact that retrieves the data in the UDDI
where the integration enabled by the issuer delivers a Portal technology
responsible for an XML operation."

The algorithm is based on a simplified English grammar, fed with hard-coded
lists of (buzz)words. The sentence structure is selected by choosing
randomly among a set of weighted rules, i.e. some rules are more likely to
be used than others. The sentences are oriented to hype Web technologies but
you can easily switch to your preferred domain, simply by changing the list
of words.

For Windows XP/Vista users: if you have installed the win32com package
(delivered with PythonWin), you should hear the sentences pronounced by
synthesized speech.

Have fun,

Pierre Denis

Instruction: simply copy the following lines in a bullshit_generator.py file
and executes the script (requires Python 2.3 at least). Press enter to get
more sentences and 'q' + enter to exit.
"""

'''
======================================================================
 Bullshit Generator
    by Pierre Denis, March 2009
======================================================================
'''

# --------------------------------------------------
# grammar engine
# --------------------------------------------------

from random import choice, random
from bisect import bisect

class Node(object):

    def setTermsChoices(self,*termsChoices):
        self.termsChoices = []
        weights = []
        for weight, termChoice in termsChoices:
            self.termsChoices.append(termChoice)
            weights.append(weight)
        totalWeight = sum(weights)
        self.thresholds = []
        threshold = 0.0
        for weight in weights[:-1]:
            threshold += weight
            self.thresholds.append(threshold/totalWeight)

    def getWords(self):
        terms = self.termsChoices[bisect(self.thresholds,random())]
        for term in terms:
            if isinstance(term,str):
                yield term
            else:
                for word in term.getWords():
                    yield word

    def getString(self):
        # note : starting from Python 2.4, the two following statements
        # may be changed to use generator expressions,
        # i.e. remove list(...) and brackets []
        res = " ".join(list(self.getWords()))
        res = ", ".join([w.strip() for w in res.split(",") if w.strip()])
        if res.endswith(", "):
            res = res[:-2]
        return res[0].upper() + res[1:] + "."


class TerminalNode(object):

    def __init__(self,*words):
        self.words = words

    def getWords(self):
        yield choice(self.words)

# --------------------------------------------------
# grammar
# --------------------------------------------------

verb = TerminalNode(
    "accesses", "activates", "administrates", "aggregates", "builds",
    "calculates", "checks", "competes with", "completes", "complies with",
    "controls", "covers", "delivers", "dispatches", "eases", "encapsulates",
    "encompasses", "executes", "extracts", "features",
    "generates", "gets", "governs", "guides", "has", "increases",
    "inherits from", "is", "keeps track of", "leverages", "makes",
    "manages",
    "manages", "maximizes", "mitigates", "monitors", "must have", "needs",
    "offers", "opens", "operates on", "optimizes", "orchestrates",
    "overwrites", "performs", "populates", "precludes", "provides",
    "provides",
    "provides an interface to", "reads", "receives", "reduces",
    "reduces the need of", "registers", "regulates", "relies on",
    "requires",
    "resides on", "resides within", "retrieves", "retrieves the data in",
    "runs on",
    "schedules", "integrates with", "sends", "shall be",
    "shall have", "should be", "should have", "starts", "stores",
    "streamlines", "subscribes to", "subscribes to", "supersedes", "takes",
    "targets", "triggers", "updates", "validates", "writes")

passiveVerb = TerminalNode(
    "accessed by", "achieved by", "aggregated by", "applicable for",
    "asserted by", "authorized by",
    "based upon", "built from", "built upon", "collected by",
    "controlled by",
    "dedicated to", "deployed on", "derived from", "dispatched by",
    "driven by", "eased by", "enabled by", "envisioned in",
    "extracted from", "generated by", "in the scope of", "installed on",
    "integrated in",
    "located in", "managed by", "maximized by", "monitored by", "opened by",
    "optimized by", "orchestrated by", "packaged in", "performed by",
    "populated by", "processed by", "provided by", "provided by",
    "received by", "refreshed by", "registered in", "related to",
    "required by",
    "responsible for", "scheduled by", "sent to", "serialized by",
    "serialized in", "started in", "stored by", "stored in", "stored on",
    "the interface of", "updated by", "validated by")

aSimpleName = TerminalNode(
    "COTS", "GRID processing",
    "Java program", "LDAP registry", "Portal", "RSS feed", "SAML token",
    "SOAP message", "SSO", "TCP/IP", "UML model", "URL",
    "W3C", "Web", "Web 2.0", "Web browser", "Web page",
    "Web service", "back-end", "backbone", "bandwidth", "bean",
    "bridge", "browser", "bus", "business", "business model", "call",
    "catalogue", "class", "client", "cluster", "collection",
    "communication", "component", "compression",
    "concept", "conceptualization", "connexion", "console", "content",
    "context", "cookie", "customization", "data", "database",
    "datastore", "deployment",
    "derivation rule", "design", "development", "device", "directory",
    "discovery", "dispatcher", "document", "domain", "factory",
    "fat client", "feature", "file", "form", "frame", "framework",
    "function", "gateway", "genericity", "geomanagement", "goal",
    "governance", "granularity", "guideline", "header", "key", "layer",
    "leader", "library", "link", "list", "log file", "logic",
    "look-and-feel",
    "manager", "market", "mechanism", "message", "meta-model",
    "metadata", "model", "modeling", "module", "network", "performance",
    "persistence", "personalization", "plug-in", "policy", "port",
    "portal", "practice",
    "presentation layer", "privacy", "private key", "procedure",
    "process", "processor", "processing", "product", "protocol",
    "recommendation",
    "registration", "registry", "relationship", "resource",
    "responsibility", "role",
    "rule", "scenario", "scenario", "scheduler", "schema", "security",
    "server", "service", "service provider", "servlet", "session",
    "skeleton", "software", "solution", "source", "space",
    "specification", "standard", "state", "statement", "streaming",
    "style sheet", "subscriber", "subsystem", "system", "system",
    "table", "target", "task", "taxonomy", "technique", "technology",
    "template", "thin client", "thread", "throughput", "timing", "tool",
    "toolkit", "topic", "unit", "usage", "use case", "user",
    "user experience", "validation", "value", "version", "vision", "work",
    "workflow")

anSimpleName = TerminalNode(
    "API", "IP address", "Internet", "UDDI", "XML", "XML file",
    "abstraction", "access", "acknowledgment", "action", "actor",
    "administrator", "aggregator", "algorithm", "application", "approach",
    "architecture", "artifact", "aspect", "authentication", "availability",
    "encapsulation", "end-point", "engine", "engine", "entity",
    "entity", "environment", "event", "identifier", "information",
    "integration", "interface", "interoperability", "issuer", "object",
    "ontology", "operation", "operator", "operator", "opportunity",
    "orchestration", "owner")

aAdjective = TerminalNode(
    "BPEL",  "DOM", "DTD", "GRID", "HTML", "J2EE",
    "Java", "Java-based", "Java-based", "UML", "SAX", "WFS", "WSDL",
    "basic", "broad", "bug-free",
    "business-driven", "client-side", "coarse", "coherent", "compatible",
    "complete", "compliant", "comprehensive", "conceptual", "consistent",
    "control", "controller", "cost-effective",
    "custom", "data-driven", "dedicated", "distributed",
    "dynamic", "encrypted", "event-driven", "fine-grained", "first-class",
    "free", "full",
    "generic", "geo-referenced", "global", "global", "graphical",
    "high-resolution", "high-level", "individual", "invulnerable",
    "just-in-time", "key",
    "layered", "leading", "lightweight", "logical", "main", "major",
    "message-based",
    "most important", "multi-tiers", "narrow", "native", "next",
    "next-generation",
    "normal", "password-protected", "operational", "peer-to-peer",
    "performant", "physical",
    "point-to-point", "polymorphic", "portable", "primary", "prime",
    "private", "proven", "public", "raw", "real-time", "registered",
    "reliable", "remote",
    "respective", "right", "robust", "rule-based", "scalable", "seamless",
    "secondary", "semantic",
    "server-side", "service-based", "service-oriented", "simple", "sole",
    "specific", "state-of-the-art", "stateless", "storage", "sufficient",
    "technical", "thread-safe", "uniform", "unique", "used", "useful",
    "user-friendly", "virtual", "visual", "web-based", "web-centric",
    "well-documented", "wireless", "world-leading", "zero-default")

anAdjective = TerminalNode(
    "AJAX", "OO", "XML-based", "abstract", "ancillary", "asynchronous",
    "authenticated", "authorized", "auto-regulated", "available", "aware",
    "efficient",
    "international", "interoperable", "off-line", "official", "online",
    "open", "operational",
    "other", "own", "unaffected", "up-to-date")

adverb = TerminalNode(
    "basically", "comprehensively", "conceptually", "consistently",
    "definitely", "dramatically",
    "dynamically", "expectedly", "fully", "generally", "generically",
    "globally", "greatly", "individually", "locally", "logically",
    "mainly", "mostly", "natively",
    "officially", "physically", "practically", "primarily",
    "repeatedly", "roughly", "sequentially", "simply", "specifically",
    "surely", "technically", "undoubtly", "usefully", "virtually")

sentenceHead = TerminalNode(
    "actually", "as a matter of fact", "as said before", "as stated before",
    "basically", "before all", "besides this", "beyond that point",
    "clearly",
    "conversely", "despite these facts", "for this reason",
    "generally speaking",
    "if needed", "in essence", "in other words", "in our opinion",
    "in the long term", "in the short term", "in this case", "incidentally",
    "moreover", "nevertheless", "now", "otherwise", "periodically",
    "roughly speaking", "that being said", "then", "therefore",
    "to summarize", "up to here", "up to now", "when this happens")

(name, aName, anName, nameTail, adjective, nameGroup,
 simpleNameGroup, verbalGroup, simpleVerbalGroup, sentence,
 sentenceTail) = [Node() for i in xrange(11)]

aName.setTermsChoices(
    ( 50, ( aSimpleName, ) ),
    (  5, ( aSimpleName, name ) ),
    (  8, ( aSimpleName, name ) ),
    (  5, ( aName, nameTail ) ) )

anName.setTermsChoices(
    ( 50, ( anSimpleName, ) ),
    (  8, ( anSimpleName, name ) ),
    (  5, ( anName, nameTail ) ) )

nameTail.setTermsChoices(
    (  2, ( "of", nameGroup ) ),
    (  2, ( "from", nameGroup ) ),
    (  1, ( "under", nameGroup ) ),
    (  1, ( "on top of", nameGroup ) ) )

name.setTermsChoices(
    (  1, ( aName, ) ),
    (  1, ( anName, ) ) )

adjective.setTermsChoices(
    (  1, ( aAdjective, ) ),
    (  1, ( anAdjective, ) ) )

nameGroup.setTermsChoices(
    ( 10, ( simpleNameGroup, ) ),
    (  1, ( simpleNameGroup, passiveVerb, nameGroup ) ),
    (  1, ( simpleNameGroup, "that", simpleVerbalGroup ) ),
    (  1, ( simpleNameGroup, ", which", simpleVerbalGroup, "," ) ) )

simpleNameGroup.setTermsChoices(
    ( 40, ( "the", name ) ),
    ( 20, ( "the", adjective, name ) ),
    ( 10, ( "a", aName ) ),
    ( 10, ( "an", anName ) ),
    (  5, ( "a", aAdjective, name ) ),
    (  5, ( "an", anAdjective, name ) ) )

verbalGroup.setTermsChoices(
    ( 10, ( verb, nameGroup ) ),
    (  1, ( adverb, verb, nameGroup ) ),
    ( 10, ( "is", passiveVerb, nameGroup ) ),
    (  1, ( "is", adverb, passiveVerb, nameGroup ) ),
    (  1, ( "is", adjective ) ),
    (  1, ( "is", adverb, adjective ) ) )

simpleVerbalGroup.setTermsChoices(
    (  2, ( verb, simpleNameGroup ) ),
    (  1, ("is", adjective ) ) )

sentence.setTermsChoices(
    ( 20, (nameGroup, verbalGroup ) ),
    (  4, (sentenceHead, "," , nameGroup, verbalGroup ) ),
    (  4, (sentence, sentenceTail ) ) )

sentenceTail.setTermsChoices(
    ( 12, ( "in", nameGroup) ),
    (  5, ( "within", nameGroup) ),
    (  5, ( "where", nameGroup, verbalGroup) ),
    (  5, ( "when", nameGroup, verbalGroup) ),
    (  2, ( "because it", verbalGroup ) ),
    (  1, ( "; that's why it", verbalGroup ) ) )

# --------------------------------------------------
# main program
# --------------------------------------------------
try:
    import win32com.client
    voice = win32com.client.Dispatch("sapi.SPVoice")
except:
    voice = None

print "press <enter> to resume, 'q'+<enter> to quit\n"


#import win32com.client
#s = win32com.client.Dispatch("SAPI.SpVoice")
#s.Speak('This is punthoofd?')

while True:
    print
    for i in xrange(8):
        generatedSentence = sentence.getString()
        print generatedSentence,
        if voice:
            voice.Speak ( generatedSentence )
    if raw_input().strip().lower() == "q":
        break


#--
#http://mail.python.org/mailman/listinfo/python-list
