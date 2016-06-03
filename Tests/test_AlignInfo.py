# Copyright 2016 by Peter Cock.  All rights reserved.
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

"""Bio.Align.AlignInfo related tests."""
import unittest

from Bio.Alphabet import DNAAlphabet, generic_protein
from Bio.Alphabet import HasStopCodon, Gapped
from Bio.Alphabet.IUPAC import unambiguous_dna
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import AlignIO
from Bio.SubsMat.FreqTable import FreqTable, FREQ
from Bio.Align.AlignInfo import SummaryInfo


class AlignInfoTests(unittest.TestCase):
    """Test basic usage."""

    def test_nucleotides(self):
        filename = "GFF/multi.fna"
        format = "fasta"
        alignment = AlignIO.read(filename, format, alphabet=unambiguous_dna)
        summary = SummaryInfo(alignment)

        c = summary.dumb_consensus(ambiguous="N")
        self.assertEqual(str(c), 'NNNNNNNN')
        self.assertNotEqual(c.alphabet, unambiguous_dna)
        self.assertTrue(isinstance(c.alphabet, DNAAlphabet))

        c = summary.gap_consensus(ambiguous="N")
        self.assertEqual(str(c), 'NNNNNNNN')
        self.assertNotEqual(c.alphabet, unambiguous_dna)
        self.assertTrue(isinstance(c.alphabet, DNAAlphabet))

        expected = FreqTable({"A": 0.25, "G": 0.25, "T": 0.25, "C": 0.25},
                             FREQ, unambiguous_dna)

        m = summary.pos_specific_score_matrix(chars_to_ignore=['-'],
                                              axis_seq=c)
        self.assertEqual(str(m), """    A   C   G   T
N  2.0 0.0 1.0 0.0
N  1.0 1.0 1.0 0.0
N  1.0 0.0 2.0 0.0
N  0.0 1.0 1.0 1.0
N  1.0 2.0 0.0 0.0
N  0.0 2.0 1.0 0.0
N  1.0 2.0 0.0 0.0
N  0.0 2.0 1.0 0.0
""")

        # Have a generic alphabet, without a declared gap char, so must tell
        # provide the frequencies and chars to ignore explicitly.
        ic = summary.information_content(e_freq_table=expected,
                                         chars_to_ignore=['-'])
        self.assertAlmostEqual(ic, 7.32029999423075, places=6)

    def test_proteins(self):
        alpha = HasStopCodon(Gapped(generic_protein, "-"), "*")
        a = MultipleSeqAlignment([
                SeqRecord(Seq("MHQAIFIYQIGYP*LKSGYIQSIRSPEYDNW-", alpha), id="ID001"),
                SeqRecord(Seq("MH--IFIYQIGYAYLKSGYIQSIRSPEY-NW*", alpha), id="ID002"),
                SeqRecord(Seq("MHQAIFIYQIGYPYLKSGYIQSIRSPEYDNW*", alpha), id="ID003")])
        self.assertEqual(32, a.get_alignment_length())

        s = SummaryInfo(a)

        c = s.dumb_consensus(ambiguous="X")
        self.assertEqual(str(c), "MHQAIFIYQIGYXXLKSGYIQSIRSPEYDNW*")

        c = s.gap_consensus(ambiguous="X")
        self.assertEqual(str(c), "MHXXIFIYQIGYXXLKSGYIQSIRSPEYXNWX")

        m = s.pos_specific_score_matrix(chars_to_ignore=['-', '*'], axis_seq=c)
        self.assertEqual(str(m), """    A   D   E   F   G   H   I   K   L   M   N   P   Q   R   S   W   Y
M  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
H  0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
X  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 0.0
X  2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
I  0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
F  0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
I  0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
Y  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0
Q  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0
I  0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
G  0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
Y  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0
X  1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 0.0 0.0
X  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 2.0
L  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
K  0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
S  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0
G  0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
Y  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0
I  0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
Q  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0
S  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0
I  0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
R  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0
S  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0
P  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0
E  0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
Y  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0
X  0.0 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
N  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 0.0
W  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 3.0 0.0
X  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
""")

        ic = s.information_content(chars_to_ignore=['-', '*'])
        self.assertAlmostEqual(ic, 133.061475107, places=6)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)