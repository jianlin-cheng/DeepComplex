//Written by Paul Stothard, University of Alberta, Canada

function proteinGravy (theDocument) {	

	var newProtein = "";
	var title = "";
	var maxInput = 500000;

	if (testScript() == false) {
		return false;
	}

	if ((checkFormElement (theDocument.forms[0].elements[0]) == false) || (checkSequenceLength(theDocument.forms[0].elements[0].value, maxInput) == false))	{
		return false;
	}
	
	openWindow("Protein GRAVY");
	var arrayOfFasta = getArrayOfFasta (theDocument.forms[0].elements[0].value);

	for (var i = 0; i < arrayOfFasta.length; i++)	{

		newProtein = getSequenceFromFasta (arrayOfFasta[i]);

		title = getTitleFromFasta (arrayOfFasta[i]);

		newProtein = removeNonProtein(newProtein);

		outputWindow.document.write(getInfoFromTitleAndSequence(title, newProtein));

		outputWindow.document.write(getProteinGravy(newProtein));
		
		outputWindow.document.write ('<br />\n<br />\n');
	}

	closeWindow();
	return true;
}


function getProteinGravy (sequence) {
	sequence = sequence.toLowerCase();
	var gravyResult = 0;
	//The GRAVY value for a peptide or protein is calculated as the sum of hydropathy values [9]
	//of all the amino acids, divided by the number of residues in the sequence. 
	var gravyValues = _getGravyHash();
	for (var i = 0; i < sequence.length; i++) {
		gravyResult = gravyResult + gravyValues[sequence.charAt(i)];
	}
	if (sequence.length > 0) {
		gravyResult = gravyResult / sequence.length;
	}
	else {
		return "The sequence is too short";
	}
	return gravyResult.toFixed(3);
}


function _getGravyHash() {
	//Author(s): Kyte J., Doolittle R.F.
	//Reference: J. Mol. Biol. 157:105-132(1982).	
	var hash = {};
	hash['a'] = 1.800;
	hash['r'] = -4.500;
	hash['n'] = -3.500;
	hash['d'] = -3.500;
	hash['c'] = 2.500;
	hash['q'] = -3.500;
	hash['e'] = -3.500;
	hash['g'] = -0.400;
	hash['h'] = -3.200;
	hash['i'] = 4.500;
	hash['l'] = 3.800;
	hash['k'] = -3.900;
	hash['m'] = 1.900;
	hash['f'] = 2.800;
	hash['p'] = -1.600;
	hash['s'] = -0.800;
	hash['t'] = -0.700;
	hash['w'] = -0.900;
	hash['y'] = -1.300;
	hash['v'] = 4.200;
	return hash;
}
