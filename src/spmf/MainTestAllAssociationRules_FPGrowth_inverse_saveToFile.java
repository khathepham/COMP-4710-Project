
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

import ca.pfv.spmf.algorithms.associationrules.agrawal94_association_rules.AlgoAgrawalFaster94;
import ca.pfv.spmf.algorithms.frequentpatterns.apriori_inverse.AlgoAprioriInverse;
import ca.pfv.spmf.patterns.itemset_array_integers_with_count.Itemsets;

/**
 * Example of how to mine all association rules with FPGROWTH and save
 * the result to a file, from the source code.
 * 
 * @author Philippe Fournier-Viger (Copyright 2008)
 */
public class MainTestAllAssociationRules_FPGrowth_inverse_saveToFile {

	public static void main(String[] arg) throws IOException {
		String input = fileToPath("pokeparse.txt");
		String output = ".//output_inverse_rules.txt";

		// By changing the following lines to some other values
		// it is possible to restrict the number of items in the antecedent and
		// consequent of rules
		int maxConsequentLength = 1500;
		int maxAntecedentLength = 1500;

		// STEP 1: Applying the FP-GROWTH algorithm to find frequent itemsets
		// Note that we set the output file path to null because
		// we want to keep the result in memory instead of saving them
		// to an output file in this example.

		// the thresholds that we will use:
		double minsup = Double.parseDouble(arg[0]);// 0.001;
		double maxsup = Double.parseDouble(arg[1]);// 0.61;

		// Applying the APRIORI-Inverse algorithm to find sporadic itemsets
		AlgoAprioriInverse apriori2 = new AlgoAprioriInverse();
		// apply the algorithm
		Itemsets patterns = apriori2.runAlgorithm(minsup, maxsup, input, null);
		int databaseSize = apriori2.getDatabaseSize();
		apriori2.printStats();

		// STEP 2: Generating all rules from the set of frequent itemsets (based on
		// Agrawal & Srikant, 94)
		double minconf = Double.parseDouble(arg[2]);// 0.6
		AlgoAgrawalFaster94 algoAgrawal = new AlgoAgrawalFaster94();
		algoAgrawal.setMaxConsequentLength(maxConsequentLength);
		algoAgrawal.setMaxAntecedentLength(maxAntecedentLength);
		algoAgrawal.runAlgorithm(patterns, output, databaseSize, minconf);
		algoAgrawal.printStats();
	}

	public static String fileToPath(String filename) throws UnsupportedEncodingException {
		URL url = MainTestAllAssociationRules_FPGrowth_inverse_saveToFile.class.getResource(filename);
		return java.net.URLDecoder.decode(url.getPath(), "UTF-8");
	}
}
