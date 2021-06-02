//Written by Paul Stothard, University of Alberta, Canada

function genbankTrans (theDocument) {	
	var maxInput = 200000;

	if (testScript() == false) {
		return false;
	}

	if ((checkFormElement (theDocument.forms[0].elements[0]) == false) || (verifyGenBankFeat (theDocument.forms[0].elements[0].value) == false) || (checkTextLength(theDocument.forms[0].elements[0].value, maxInput) == false))	{
		return false;
	}

	openWindow("GenBank Trans Extractor");
	openPre();
	genBankTransExtract(theDocument.forms[0].elements[0].value);	
	closePre();
	closeWindow();
	return true;
}
function genBankTransExtract (genBankFile)	{
	genBankFile = "_" + genBankFile + "_";
	var recordArray = genBankFile.split(/LOCUS\s\s\s[^\f\n\r]*/m);
	for (var i=1; i < recordArray.length; i++) {
		var mainArray = recordArray[i].split(/DEFINITION|ACCESSION|FEATURES|ORIGIN[^\f\n\r]*/);
		var title = filterFastaTitle(mainArray[1].replace(/[\f\n\r\t]+$/g, "")) + "\n";
		var dnaSequenceArray = mainArray[4].split (/\/{2}/);
		outputWindow.document.write (title + "\n");
		if (dnaSequenceArray.length == 1) {
			alert ("The entire GenBank file may not have been processed.");
			outputWindow.focus();
		}
		var featureArray = mainArray[3].split(/[\f\n\r] {5,12}\b/);
		showFeatureTrans (featureArray);
	}
	return true;

}

function showFeatureTrans (arrayOfFeatures)	{
	var featureTitle = "";
	var theTitle = "";
	var removedTitle = "";
	var firstQualifier = "";
	var translation = "";
	var translationFound = false;
	for (var i=1; i < arrayOfFeatures.length; i++) {
		if (arrayOfFeatures[i].search(/\/translation/) != -1)	{
			arrayOfFeatures[i] = arrayOfFeatures[i].replace(/[\[\]\*]/g,"");
			featureTitle = (arrayOfFeatures[i].match(/[^ \f\n\r\t\v]+ /)).toString(); 
			theTitle = new RegExp (featureTitle);
			removedTitle = arrayOfFeatures[i].replace(theTitle,"");
			firstQualifier = (arrayOfFeatures[i].match(/\/[^\f\n\r]+/)).toString();
			outputWindow.document.write ('&gt;' + filterFastaTitle(featureTitle) + filterFastaTitle(firstQualifier) + "\n");
			translation = arrayOfFeatures[i].match(/\/translation="[^"]+"/);
			translation = translation.toString();
			translation = translation.replace(/\/translation/,"");
			translation = removeNonProtein(translation);
			translation = addReturns(translation);
			outputWindow.document.write(translation);
			translationFound = true;
			outputWindow.document.write('\n\n');
		}
	}
	if (translationFound == false)	{
		outputWindow.document.write('No translations were found.\n');
	}
	return true;
}
