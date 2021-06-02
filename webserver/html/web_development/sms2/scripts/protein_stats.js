//Written by Paul Stothard, University of Alberta, Canada

function proteinStats (theDocument) {	

	var newProtein = "";
	var title = "";
	var maxInput = 500000;

	if (testScript() == false) {
		return false;
	}

	if ((checkFormElement (theDocument.forms[0].elements[0]) == false) || (checkSequenceLength(theDocument.forms[0].elements[0].value, maxInput) == false))	{
		return false;
	}
	
	var itemsToCheck = ["/A/ (A)1", "/B/ (B)1", "/C/ (C)1", "/D/ (D)1", "/E/ (E)1", "/F/ (F)1", "/G/ (G)1", "/H/ (H)1", "/I/ (I)1", "/K/ (K)1", "/L/ (L)1", "/M/ (M)1", "/N/ (N)1", "/P/ (P)1", "/Q/ (Q)1", "/R/ (R)1", "/S/ (S)1", "/T/ (T)1", "/V/ (V)1", "/W/ (W)1", "/X/ (X)1", "/Y/ (Y)1", "/Z/ (Z)1", "/[GAVLI]/ (Aliphatic G,A,V,L,I)1", "/[FWY]/ (Aromatic F,W,Y)1", "/[CM]/ (Sulphur C,M)1", "/[KRH]/ (Basic K,R,H)1", "/[BDENQZ]/ (Acidic B,D,E,N,Q,Z)1", "/[ST]/ (Aliphatic hydroxyl S,T)1", "/[ZEQRCMVILYW]/ (tRNA synthetase class I Z,E,Q,R,C,M,V,I,L,Y,W)1", "/[BGAPSTHDNKF]/ (tRNA synthetase class II B,G,A,P,S,T,H,D,N,K,F)1"];
	
	openWindow("Protein Stats");
	var arrayOfFasta = getArrayOfFasta (theDocument.forms[0].elements[0].value);

	for (var i = 0; i < arrayOfFasta.length; i++)	{

		newProtein = getSequenceFromFasta (arrayOfFasta[i]);

		title = getTitleFromFasta (arrayOfFasta[i]);

		newProtein = removeNonProteinAllowDegen(newProtein);

		outputWindow.document.write(getInfoFromTitleAndSequence(title, newProtein));

		writeSequenceStats (newProtein, itemsToCheck);
		
		outputWindow.document.write ('<br />\n<br />\n');
	}

	closeWindow();
	return true;
}



