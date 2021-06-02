//Written by Paul Stothard, University of Alberta, Canada

function genbankFeat (theDocument) {	
	var maxInput = 1000000;

	if (testScript() == false) {
		return false;
	}

	if ((checkFormElement (theDocument.forms[0].elements[0]) == false) || (verifyGenBankFeat (theDocument.forms[0].elements[0].value) == false) || (checkTextLength(theDocument.forms[0].elements[0].value, maxInput) == false))	{
		return false;
	}

	openWindow("GenBank Feature Extractor");
	openPre();
	genBankFeatExtract(theDocument.forms[0].elements[0].value, theDocument.forms[0].elements[4].options[theDocument.forms[0].elements[4].selectedIndex].value);	
	closePre();
	closeWindow();
	return true;
}

function genBankFeatExtract (genBankFile,outputType)	{
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
		var dnaSequence = removeNonDna(dnaSequenceArray[0]);
		var featureArray = mainArray[3].split(/[\f\n\r] {5,12}\b/);		
		prepareFeatures (featureArray,dnaSequence,outputType);
	}
	return true;
}

function prepareFeatures (arrayOfFeatures,dnaSequence,outputType)	{
	var featureTitle = "";
	var theTitle = "";
	var removedTitle = "";
	var firstQualifier = "";
	var position = "";
	var positionNoSpace = "";
	var featureFound = false;
	for (var i=1; i < arrayOfFeatures.length; i++) {
		arrayOfFeatures[i] = arrayOfFeatures[i].replace(/[\[\]\*]/g,"");
		featureTitle = (arrayOfFeatures[i].match(/[^ \f\n\r\t\v]+ /)).toString();
		theTitle = new RegExp (featureTitle);
		removedTitle = arrayOfFeatures[i].replace(theTitle,"");
		if (arrayOfFeatures[i].search(/\/[^\f\n\r]+/) != -1)	{
			firstQualifier = (arrayOfFeatures[i].match(/\/[^\f\n\r]+/)).toString();
		}
		else	{
			firstQualifier = '/no qualifier supplied';
		}
		position = removedTitle.split(/\//);
		positionNoSpace = position[0].replace(/\s{2,}/g," ");
		outputWindow.document.write ('&gt;' + filterFastaTitle(featureTitle) + filterFastaTitle(firstQualifier) + "\n");
		printFeature(positionNoSpace,dnaSequence,outputType);
		featureFound = true;
		outputWindow.document.write('\n\n');
	}
	if (featureFound == false)	{
		outputWindow.document.write('There were no features found or there was a problem reading the feature information.');
	}
	return true;
}

function printFeature(featurePos,dnaSequence,outputType)	{
	var feature;
	featurePos = featurePos.replace(/<|>/g,"");
	if ((featurePos.search(/[^a-z\d\.\(\)\,\s]/) != -1) || (featurePos.search(/one/) != -1) || (featurePos.search(/order/) != -1))	{
		outputWindow.document.write ('This feature specifies a sequence that cannot be represented:\n');
		outputWindow.document.write (featurePos);
	}
	else	{


		var newFeaturePos = featurePos.replace(/\)/g,"");
		if (newFeaturePos.search(/complement/) != -1)	{
			feature = new Feature("complement");
		}
		else {
			feature = new Feature("direct");
		}		

		var posArray = newFeaturePos.split(/\(/);
		var last = posArray.length - 1;	
		var pairString = posArray[last];	
		var pairArray = pairString.split(/\,/);
		var digitArray = new Array();
		var realStart = 0;
		var realStop = 0;

		for (var j = 0; j < pairArray.length; j++)	{
			digitArray = pairArray[j].split(/\.\./);
			if (digitArray.length == 1)	{
				digitArray[1] = digitArray[0];
			}
			realStart = digitArray[0];
			realStop = digitArray[1];
			realStop = realStop.replace(/\D/g,"");
			realStart = realStart.replace(/\D/g,"");
			if ((realStart.search(/\d/) == -1) || (realStop.search(/\d/) == -1))	{
				outputWindow.document.write ('There was a problem with this feature (one of the range values was missing).');
				return true;
			}
			realStart = parseInt(realStart) - 1;
			realStop = parseInt(realStop);
			if (realStart > realStop)	{
				outputWindow.document.write ('There was a problem with this feature (the end position was before the start position).');
				return true;
			}
			if ((realStart > dnaSequence.length) || (realStop > dnaSequence.length))	{
				outputWindow.document.write ('The entire GenBank file was not processed, so this feature cannot be properly shown.'); //to handle case where web browser limits the number of characters that can be entered as input.
				return true;
			}
			else	{
				
				if (outputType == "separated")	{
					feature.addFragment(dnaSequence.substring(realStart,realStop));
				}
				else	{
					feature.addFragment (dnaSequence.substring(feature.lastAdded, realStart));
					feature.addFragment ((dnaSequence.substring(realStart, realStop)).toUpperCase());
					feature.lastAdded = realStop;
				}
			}
		}
		feature.writeFeature();
	}
	return true;
}


//class Feature method writeFeature()
function writeFeature() {
	if (this.strand == "complement") {
		outputWindow.document.write(addReturns(reverse(complement(this.fragments.join("")))));
	}
	else {
		outputWindow.document.write(addReturns(this.fragments.join("")));
	}
}

//class Feature method addFragment()
function addFragment(sequence) {
	this.fragments.push(sequence);
}

//class Feature
function Feature (strand) {
	this.strand = strand;
	this.fragments = new Array();
	this.lastAdded = 0;
}

//create and throw away a prototype object
new Feature();

// define object methods
Feature.prototype.writeFeature = writeFeature;
Feature.prototype.addFragment = addFragment;
