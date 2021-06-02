//Written by Paul Stothard, University of Alberta, Canada

function colorAlignProp (theDocument,formid) {
	var maxInput = 200000;	

	if (testScript() == false) {
		return false;
	}

	var theAlignment = "";
	var alignArray = new Array();
	var groupString = "";
	var arrayOfGroups = new Array();

	var titleArray = new Array();
	var sequenceArray = new Array();

	var longestTitle;

	//if ((checkFormElement (theDocument.forms[0].elements[0]) == false) || (checkTextLength(theDocument.forms[0].elements[0].value, maxInput) == false))	{
	if ((checkFormElement (theDocument.getElementById(formid).elements[0]) == false) || (checkTextLength(theDocument.getElementById(formid).elements[0].value, maxInput) == false))	{
		return false;
	}

	theAlignment = "X" + theDocument.getElementById(formid).elements[0].value;
	//alert(theAlignment);
	alignArray = theAlignment.split(/[>%#]/);

	if (earlyCheckAlign (alignArray) == false)	{
		return false;
	}

	for (var i = 1; i < alignArray.length; i++)	{
		titleArray[i-1] = alignArray[i].match(/[^\f\n\r]+[\f\n\r]/);
		titleArray[i-1] = filterFastaTitle(titleArray[i-1].toString()).replace(/[\f\n\r]/g, "");
		titleArray[i-1] = titleArray[i-1].substring(0, 20);
		if (i == 1) {
			longestTitle = titleArray[i-1].length;
		}
		else if (titleArray[i-1].length > longestTitle)	{
			longestTitle = titleArray[i-1].length;
		}
		sequenceArray[i-1] = alignArray[i].replace(/[^\f\n\r]+[\f\n\r]/,"");
		sequenceArray[i-1] = filterAlignSeqAllowAsterisk (sequenceArray[i-1]);
	}

	//make titles equal length
	var spaceString = "                    ";
	for (var i = 0; i < titleArray.length; i++)	{
		if (titleArray[i].length < longestTitle) {
			//add spaces
			titleArray[i] = titleArray[i] + spaceString.substring(0, (longestTitle - titleArray[i].length));
		}
	}

	if (checkAlign (titleArray, sequenceArray) == false)	{
		return false;
	}

	groupString = (("GAVLI, FYW, CM, ST, KRH, DE, NQ, P").replace(/\s/g,"")).toUpperCase();
	arrayOfGroups = groupString.split(/,/);
	if (checkGroupInput (arrayOfGroups) == false)	{
		return false;
	}

	var isBackground;
	//if (theDocument.forms[0].elements[6].options[theDocument.forms[0].elements[6].selectedIndex].value == 'background') {
	if (theDocument.getElementById(formid).elements[6].options[theDocument.getElementById(formid).elements[6].selectedIndex].value == 'background') {
	    isBackground = true;
	}
	else {
	    isBackground = false;
	}

	//_openWindowAlign("Color Align Properties", isBackground);
	_openWindowAlign("Local alignment", isBackground);
	
	openPre();
	outputWindow.document.write("<span class=\"g\">" + "G, A, V, L, I" + "</span>\n");
	outputWindow.document.write("<span class=\"f\">" + "F, Y, W" + "</span>\n");
	outputWindow.document.write("<span class=\"c\">" + "C, M" + "</span>\n");
	outputWindow.document.write("<span class=\"s\">" + "S, T" + "</span>\n");
	outputWindow.document.write("<span class=\"k\">" + "K, R, H" + "</span>\n");
	outputWindow.document.write("<span class=\"d\">" + "D, E" + "</span>\n");
	outputWindow.document.write("<span class=\"q\">" + "N, Q" + "</span>\n");
	outputWindow.document.write("<span class=\"p\">" + "P" + "</span>\n");
	outputWindow.document.write("\n");
	//colorAlign (titleArray, sequenceArray, theDocument.forms[0].elements[4].options[theDocument.forms[0].elements[4].selectedIndex].value, theDocument.forms[0].elements[5].options[theDocument.forms[0].elements[5].selectedIndex].value, arrayOfGroups, theDocument.forms[0].elements[7].value, longestTitle);
	colorAlign (titleArray, sequenceArray, theDocument.getElementById(formid).elements[4].options[theDocument.getElementById(formid).elements[4].selectedIndex].value, theDocument.getElementById(formid).elements[5].options[theDocument.getElementById(formid).elements[5].selectedIndex].value, arrayOfGroups, theDocument.getElementById(formid).elements[7].value, longestTitle);
	
	outputWindow.document.write("The Sequence Manipulation Suite Copyright &copy; 2000, 2004 Paul Stothard.\n");
	closePre();
	closeWindow();
	return true;
}

function colorAlign (arrayOfTitles, arrayOfSequences, basePerLine, consensus, arrayOfGroups, definedStarts, longestTitle)	{
	var positions = new Array (arrayOfSequences.length);
	if (definedStarts.search(/\S/) == -1)	{
		definedStarts = "0,0";
	}
	var definedStartsArray = definedStarts.split(/,/);
	for (var i = 0; i < positions.length; i++)	{
		if (i >= definedStartsArray.length)	{
			positions[i] = 0;
		}
		else	{
			if (definedStartsArray[i].search(/\d/) != -1)	{
                                positions[i] = parseInt(definedStartsArray[i].replace(/[^\d\-]/g, ""));
			}
			else	{
				alert('An incorrect starting position was encountered. It was set to 0.');
				outputWindow.focus();
				positions[i] = 0;
			}
		}
	}
	var totalBasesShown = 0; 
	consensus = (parseInt(consensus)) / 100;
	basePerLine = parseInt(basePerLine);
	var columnCount = 0;
 	var arrayOfColumns = new Array(basePerLine);
	for (var i=0; i < arrayOfColumns.length; i++) {
   		arrayOfColumns[i] = new Array(arrayOfSequences.length);
	}

	var i = 0;
	var columnSeq;
	var re;
	var result;
	var output = "";

	while (totalBasesShown < arrayOfSequences[0].length)	{
		for (var jj = 0; jj < arrayOfSequences.length; jj++)	{		
			output = output + arrayOfTitles[jj] + ' ';
			while ((i < (totalBasesShown + basePerLine)) && (i < arrayOfSequences[0].length))	{
				if (jj == 0) {
					//fill the column
					for (var k = 0; k < arrayOfSequences.length; k++)	{
						arrayOfColumns[columnCount][k] = arrayOfSequences[k].charAt(i);
						
					}
				}
				if ( (arrayOfSequences[jj].charAt(i) == ".") || (arrayOfSequences[jj].charAt(i) == "-") || (arrayOfSequences[jj].charAt(i) == "*") ) {
					output = output + arrayOfSequences[jj].charAt(i);
					i = i + 1;
					columnCount++;
					continue;
				}

				columnSeq = arrayOfColumns[columnCount].join(",");
				re = new RegExp (arrayOfSequences[jj].charAt(i),"gi");				
				if ((columnSeq.match(re)).length / arrayOfSequences.length >= consensus)	{
					output = output + "<span class=\"" + arrayOfSequences[jj].charAt(i).toString().toLowerCase() + "\">" + arrayOfSequences[jj].charAt(i) + "</span>";
					i = i + 1;
					columnCount++;
					continue;
				}

				result = 1;
				for (var m = 0; m < arrayOfGroups.length; m++)	{
					if (arrayOfGroups[m].search(re) != -1)	{
						var re = new RegExp ("[" + arrayOfGroups[m] + "]","gi");
						result = (columnSeq.match(re)).length;
						break;
					}
				}

				if (result / arrayOfSequences.length >= consensus)	{
					output = output + "<span class=\"" + arrayOfSequences[jj].charAt(i).toString().toLowerCase() + "\">" + arrayOfSequences[jj].charAt(i) + "</span>";
					i = i + 1;
					columnCount++;
					continue;
				}
									
				output = output + arrayOfSequences[jj].charAt(i);
				i = i + 1;
				columnCount++;
			}
			positions[jj] = positions[jj] + ((arrayOfSequences[jj].substring(totalBasesShown,i)).replace(/\.|\-/g,"")).length;
			output = output + ' ' + positions[jj] + '\n';
			outputWindow.document.write(output);
			output = "";
			i = totalBasesShown;
			columnCount = 0;
		}
		totalBasesShown = totalBasesShown + basePerLine;
		i = totalBasesShown;
		outputWindow.document.write('\n');
	}
	return true;
}
