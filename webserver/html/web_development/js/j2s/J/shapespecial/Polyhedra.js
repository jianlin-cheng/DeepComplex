Clazz.declarePackage ("J.shapespecial");
Clazz.load (["J.shape.AtomShape", "JU.AU", "$.P3", "$.V3"], "J.shapespecial.Polyhedra", ["java.lang.Boolean", "$.Float", "java.util.Hashtable", "JU.BS", "$.Lst", "$.Measure", "$.P4", "$.PT", "$.SB", "J.c.PAL", "J.shapespecial.Polyhedron", "JU.BSUtil", "$.C", "$.Logger", "$.Normix"], function () {
c$ = Clazz.decorateAsClass (function () {
this.otherAtoms = null;
this.normalsT = null;
this.planesT = null;
this.polyhedronCount = 0;
this.polyhedrons = null;
this.drawEdges = 0;
this.radius = 0;
this.nVertices = 0;
this.faceCenterOffset = 0;
this.isCollapsed = false;
this.iHaveCenterBitSet = false;
this.bondedOnly = false;
this.haveBitSetVertices = false;
this.centers = null;
this.bsVertices = null;
this.bsVertexCount = null;
this.useUnitCell = false;
this.nPoints = 0;
this.planarParam = 0;
this.info = null;
this.distanceRef = 0;
this.buildMode = 0;
this.vAB = null;
this.vAC = null;
this.vBC = null;
Clazz.instantialize (this, arguments);
}, J.shapespecial, "Polyhedra", J.shape.AtomShape);
Clazz.prepareFields (c$, function () {
this.otherAtoms =  new Array (498);
this.normalsT =  new Array (251);
this.planesT = JU.AU.newInt2 (250);
this.polyhedrons =  new Array (32);
this.vAB =  new JU.V3 ();
this.vAC =  new JU.V3 ();
this.vBC =  new JU.V3 ();
});
Clazz.overrideMethod (c$, "setProperty", 
function (propertyName, value, bs) {
if ("init" === propertyName) {
this.faceCenterOffset = 0.25;
this.planarParam = NaN;
this.radius = 0.0;
this.nVertices = 0;
this.nPoints = 0;
this.bsVertices = null;
this.useUnitCell = false;
this.centers = null;
this.info = null;
this.bsVertexCount =  new JU.BS ();
this.bondedOnly = this.isCollapsed = this.iHaveCenterBitSet = false;
this.haveBitSetVertices = false;
if (Boolean.TRUE === value) this.drawEdges = 0;
return;
}if ("generate" === propertyName) {
if (!this.iHaveCenterBitSet) {
this.centers = bs;
this.iHaveCenterBitSet = true;
}this.deletePolyhedra ();
this.buildPolyhedra ();
return;
}if ("collapsed" === propertyName) {
this.isCollapsed = (value).booleanValue ();
return;
}if ("nVertices" === propertyName) {
var n = (value).intValue ();
if (n < 0) {
if (-n >= this.nVertices) {
this.bsVertexCount.setBits (this.nVertices, 1 - n);
this.nVertices = -n;
}} else {
this.bsVertexCount.set (this.nVertices = n);
}return;
}if ("centers" === propertyName) {
this.centers = value;
this.iHaveCenterBitSet = true;
return;
}if ("unitCell" === propertyName) {
this.useUnitCell = true;
return;
}if ("to" === propertyName) {
this.bsVertices = value;
return;
}if ("toBitSet" === propertyName) {
this.bsVertices = value;
this.haveBitSetVertices = true;
return;
}if ("toVertices" === propertyName) {
var points = value;
this.nPoints = Math.min (points.length, 250);
for (var i = this.nPoints; --i >= 0; ) this.otherAtoms[i] = points[i];

return;
}if ("faceCenterOffset" === propertyName) {
this.faceCenterOffset = (value).floatValue ();
return;
}if ("distanceFactor" === propertyName) {
return;
}if ("planarParam" === propertyName) {
this.planarParam = (value).floatValue ();
return;
}if ("bonds" === propertyName) {
this.bondedOnly = true;
return;
}if ("info" === propertyName) {
this.info = value;
this.centers = JU.BSUtil.newAndSetBit (this.info.get ("atomIndex").intValue);
this.iHaveCenterBitSet = true;
return;
}if ("delete" === propertyName) {
if (!this.iHaveCenterBitSet) this.centers = bs;
this.deletePolyhedra ();
return;
}if ("on" === propertyName) {
if (!this.iHaveCenterBitSet) this.centers = bs;
this.setVisible (true);
return;
}if ("off" === propertyName) {
if (!this.iHaveCenterBitSet) this.centers = bs;
this.setVisible (false);
return;
}if ("noedges" === propertyName) {
this.drawEdges = 0;
return;
}if ("edges" === propertyName) {
this.drawEdges = 1;
return;
}if ("frontedges" === propertyName) {
this.drawEdges = 2;
return;
}if (propertyName.indexOf ("color") == 0) {
bs = ("colorThis" === propertyName && this.iHaveCenterBitSet ? this.centers : this.andBitSet (bs));
var colixEdge = ("colorPhase" === propertyName ? JU.C.getColix (((value)[0]).intValue ()) : 0);
for (var i = this.polyhedronCount; --i >= 0; ) if (bs.get (this.polyhedrons[i].centralAtom.i)) this.polyhedrons[i].colixEdge = colixEdge;

if ("colorPhase" === propertyName) value = (value)[1];
propertyName = "color";
}if (propertyName.indexOf ("translucency") == 0) {
bs = ("translucentThis".equals (value) && this.iHaveCenterBitSet ? this.centers : this.andBitSet (bs));
if (value.equals ("translucentThis")) value = "translucent";
}if ("radius" === propertyName) {
this.radius = (value).floatValue ();
return;
}if (propertyName === "deleteModelAtoms") {
var modelIndex = ((value)[2])[0];
for (var i = this.polyhedronCount; --i >= 0; ) {
this.polyhedrons[i].info = null;
var mi = this.polyhedrons[i].centralAtom.mi;
if (mi == modelIndex) {
this.polyhedronCount--;
this.polyhedrons = JU.AU.deleteElements (this.polyhedrons, i, 1);
}}
}this.setPropAS (propertyName, value, bs);
}, "~S,~O,JU.BS");
Clazz.overrideMethod (c$, "getProperty", 
function (propertyName, index) {
if (propertyName === "symmetry") {
var s = "";
for (var i = this.polyhedronCount; --i >= 0; ) s += this.polyhedrons[i].getSymmetry (this.vwr, true) + "\n";

return s;
}return null;
}, "~S,~N");
Clazz.overrideMethod (c$, "getPropertyData", 
function (property, data) {
var iatom;
if (property === "points") {
iatom = (data[0]).intValue ();
for (var i = this.polyhedronCount; --i >= 0; ) {
if (this.polyhedrons[i].centralAtom.i == iatom) {
if (this.polyhedrons[i].collapsed) break;
data[1] = this.polyhedrons[i].vertices;
return true;
}}
return false;
}if (property === "move") {
var mat = data[1];
if (mat == null) return false;
var bs = data[0];
for (var i = this.polyhedronCount; --i >= 0; ) {
var p = this.polyhedrons[i];
if (bs.get (p.centralAtom.i)) p.move (mat);
}
return true;
}if (property === "centers") {
var bs =  new JU.BS ();
var smiles = data[1];
var sm = (smiles == null ? null : this.vwr.getSmilesMatcher ());
var n = data[0];
if (sm != null) smiles = sm.cleanSmiles (smiles);
var nv = (smiles != null ? JU.PT.countChar (smiles, '*') : n == null ? -2147483648 : n.intValue ());
if (smiles != null && nv == 0) nv = -2147483648;
for (var i = this.polyhedronCount; --i >= 0; ) {
if (nv > 0 && this.polyhedrons[i].nVertices != nv || nv > -2147483648 && nv < 0 && this.polyhedrons[i].triangles.length != -nv) continue;
if (smiles == null) {
bs.set (this.polyhedrons[i].centralAtom.i);
} else if (sm != null) {
this.polyhedrons[i].getSymmetry (this.vwr, false);
var smiles0 = this.polyhedrons[i].polySmiles;
try {
if (sm.areEqual (smiles, smiles0) > 0) bs.set (this.polyhedrons[i].centralAtom.i);
} catch (e) {
if (Clazz.exceptionOf (e, Exception)) {
e.printStackTrace ();
} else {
throw e;
}
}
}}
data[2] = bs;
return true;
}if (property === "allInfo") {
var info =  new JU.Lst ();
for (var i = this.polyhedronCount; --i >= 0; ) info.addLast (this.polyhedrons[i].getInfo (this.vwr, true));

data[1] = info;
return false;
}if (property === "info") {
iatom = (data[0]).intValue ();
for (var i = this.polyhedronCount; --i >= 0; ) {
if (this.polyhedrons[i].centralAtom.i == iatom) {
data[1] = this.polyhedrons[i].getInfo (this.vwr, true);
return true;
}}
return false;
}return false;
}, "~S,~A");
Clazz.overrideMethod (c$, "getShapeDetail", 
function () {
var lst =  new JU.Lst ();
for (var i = 0; i < this.polyhedronCount; i++) lst.addLast (this.polyhedrons[i].getInfo (this.vwr, true));

return lst;
});
Clazz.defineMethod (c$, "andBitSet", 
 function (bs) {
var bsCenters =  new JU.BS ();
for (var i = this.polyhedronCount; --i >= 0; ) bsCenters.set (this.polyhedrons[i].centralAtom.i);

bsCenters.and (bs);
return bsCenters;
}, "JU.BS");
Clazz.defineMethod (c$, "deletePolyhedra", 
 function () {
var newCount = 0;
var pid = J.c.PAL.pidOf (null);
for (var i = 0; i < this.polyhedronCount; ++i) {
var p = this.polyhedrons[i];
var iAtom = p.centralAtom.i;
if (this.centers.get (iAtom)) this.setColixAndPalette (0, pid, iAtom);
 else this.polyhedrons[newCount++] = p;
}
for (var i = newCount; i < this.polyhedronCount; ++i) this.polyhedrons[i] = null;

this.polyhedronCount = newCount;
});
Clazz.defineMethod (c$, "setVisible", 
 function (visible) {
for (var i = this.polyhedronCount; --i >= 0; ) {
var p = this.polyhedrons[i];
if (p != null && this.centers.get (p.centralAtom.i)) p.visible = visible;
}
}, "~B");
Clazz.defineMethod (c$, "buildPolyhedra", 
 function () {
var useBondAlgorithm = this.radius == 0 || this.bondedOnly;
this.buildMode = (this.info != null ? 6 : this.nPoints > 0 ? 2 : this.haveBitSetVertices ? 4 : this.useUnitCell ? 5 : useBondAlgorithm ? 1 : 3);
var iter = (this.buildMode == 3 ? this.ms.getSelectedAtomIterator (null, false, false, false, false) : null);
for (var i = this.centers.nextSetBit (0); i >= 0; i = this.centers.nextSetBit (i + 1)) {
var atom = this.atoms[i];
var p = null;
switch (this.buildMode) {
case 4:
p = this.constructBitSetPolyhedron (atom);
break;
case 5:
p = this.constructUnitCellPolygon (atom, useBondAlgorithm);
break;
case 1:
p = this.constructBondsPolyhedron (atom, 0);
break;
case 3:
this.vwr.setIteratorForAtom (iter, i, this.radius);
p = this.constructRadiusPolyhedron (atom, iter);
break;
case 6:
p =  new J.shapespecial.Polyhedron ().setInfo (this.info, this.vwr.ms.at);
break;
case 2:
p = this.validatePolyhedron (atom, this.nPoints);
break;
}
if (p != null) {
if (this.polyhedronCount == this.polyhedrons.length) this.polyhedrons = JU.AU.doubleLength (this.polyhedrons);
this.polyhedrons[this.polyhedronCount++] = p;
}if (this.haveBitSetVertices) break;
}
if (iter != null) iter.release ();
});
Clazz.defineMethod (c$, "constructBondsPolyhedron", 
 function (atom, otherAtomCount) {
if (otherAtomCount == 0) {
var bonds = atom.bonds;
if (bonds == null) return null;
var r2 = this.radius * this.radius;
for (var i = bonds.length; --i >= 0; ) {
var bond = bonds[i];
if (!bond.isCovalent ()) continue;
var other = bond.getOtherAtom (atom);
if (this.bsVertices != null && !this.bsVertices.get (other.i) || this.radius > 0 && other.distanceSquared (atom) > r2) continue;
this.otherAtoms[otherAtomCount++] = other;
if (otherAtomCount >= 250) break;
}
}this.distanceRef = 0;
return (otherAtomCount < 3 || otherAtomCount >= 250 || this.nVertices > 0 && !this.bsVertexCount.get (otherAtomCount) ? null : this.validatePolyhedron (atom, otherAtomCount));
}, "JM.Atom,~N");
Clazz.defineMethod (c$, "constructUnitCellPolygon", 
 function (atom, useBondAlgorithm) {
var unitcell = this.vwr.ms.getUnitCellForAtom (atom.i);
if (unitcell == null) return null;
var bsAtoms = JU.BSUtil.copy (this.vwr.getModelUndeletedAtomsBitSet (atom.mi));
if (this.bsVertices != null) bsAtoms.and (this.bsVertices);
if (bsAtoms.isEmpty ()) return null;
var iter = unitcell.getIterator (this.vwr, atom, this.atoms, bsAtoms, useBondAlgorithm ? 5 : this.radius);
if (!useBondAlgorithm) return this.constructRadiusPolyhedron (atom, iter);
var myBondingRadius = atom.getBondingRadius ();
if (myBondingRadius == 0) return null;
var bondTolerance = this.vwr.getFloat (570425348);
var minBondDistance = this.vwr.getFloat (570425364);
var minBondDistance2 = minBondDistance * minBondDistance;
var otherAtomCount = 0;
outer : while (iter.hasNext ()) {
var other = this.atoms[iter.next ()];
var otherRadius = other.getBondingRadius ();
var pt = iter.getPosition ();
var distance2 = atom.distanceSquared (pt);
if (!this.vwr.ms.isBondable (myBondingRadius, otherRadius, distance2, minBondDistance2, bondTolerance)) continue;
for (var i = 0; i < otherAtomCount; i++) if (this.otherAtoms[i].distanceSquared (pt) < 0.01) continue outer;

this.otherAtoms[otherAtomCount++] = pt;
if (otherAtomCount >= 250) break;
}
return this.constructBondsPolyhedron (atom, otherAtomCount);
}, "JM.Atom,~B");
Clazz.defineMethod (c$, "constructBitSetPolyhedron", 
 function (atom) {
this.bsVertices.clear (atom.i);
var otherAtomCount = 0;
this.distanceRef = 0;
for (var i = this.bsVertices.nextSetBit (0); i >= 0; i = this.bsVertices.nextSetBit (i + 1)) this.otherAtoms[otherAtomCount++] = this.atoms[i];

return this.validatePolyhedron (atom, otherAtomCount);
}, "JM.Atom");
Clazz.defineMethod (c$, "constructRadiusPolyhedron", 
 function (atom, iter) {
var otherAtomCount = 0;
this.distanceRef = this.radius;
var r2 = this.radius * this.radius;
outer : while (iter.hasNext ()) {
var other = this.atoms[iter.next ()];
var pt = iter.getPosition ();
if (pt == null) {
pt = other;
if (this.bsVertices != null && !this.bsVertices.get (other.i) || atom.distanceSquared (pt) > r2) continue;
}if (other.altloc != atom.altloc && other.altloc.charCodeAt (0) != 0 && atom.altloc.charCodeAt (0) != 0) continue;
if (otherAtomCount == 250) break;
for (var i = 0; i < otherAtomCount; i++) if (this.otherAtoms[i].distanceSquared (pt) < 0.01) continue outer;

this.otherAtoms[otherAtomCount++] = pt;
}
return (otherAtomCount < 3 || this.nVertices > 0 && !this.bsVertexCount.get (otherAtomCount) ? null : this.validatePolyhedron (atom, otherAtomCount));
}, "JM.Atom,J.api.AtomIndexIterator");
Clazz.defineMethod (c$, "validatePolyhedron", 
 function (centralAtom, vertexCount) {
var points = this.otherAtoms;
var collapsed = this.isCollapsed;
var triangleCount = 0;
var nPoints = vertexCount + 1;
var ni = vertexCount - 2;
var nj = vertexCount - 1;
var planarParam = (Float.isNaN (this.planarParam) ? 0.98 : this.planarParam);
points[vertexCount] = centralAtom;
var ptAve = JU.P3.newP (centralAtom);
for (var i = 0; i < vertexCount; i++) ptAve.add (points[i]);

ptAve.scale (1 / (vertexCount + 1));
var ptRef = JU.P3.newP (ptAve);
var bsThroughCenter =  new JU.BS ();
for (var pt = 0, i = 0; i < ni; i++) for (var j = i + 1; j < nj; j++) for (var k = j + 1; k < vertexCount; k++, pt++) if (this.isPlanar (points[i], points[j], points[k], ptRef)) bsThroughCenter.set (pt);



var triangles = this.planesT;
var pTemp =  new JU.P4 ();
var nTemp =  new JU.V3 ();
var offset = this.faceCenterOffset;
var fmax = 247;
var vmax = 250;
var bsTemp = JU.Normix.newVertexBitSet ();
var normals = this.normalsT;
var htNormMap =  new java.util.Hashtable ();
var htEdgeMap =  new java.util.Hashtable ();
var bsCenterPlanes =  new JU.BS ();
var vAC = this.vAC;
for (var i = 0, pt = 0; i < ni; i++) for (var j = i + 1; j < nj; j++) {
for (var k = j + 1; k < vertexCount; k++, pt++) {
if (triangleCount >= fmax) {
JU.Logger.error ("Polyhedron error: maximum face(" + fmax + ") -- reduce RADIUS");
return null;
}if (nPoints >= vmax) {
JU.Logger.error ("Polyhedron error: maximum vertex count(" + vmax + ") -- reduce RADIUS");
return null;
}var isThroughCenter = bsThroughCenter.get (pt);
var rpt = (isThroughCenter ? J.shapespecial.Polyhedra.randomPoint : ptAve);
var normal =  new JU.V3 ();
var isWindingOK = JU.Measure.getNormalFromCenter (rpt, points[i], points[j], points[k], !isThroughCenter, normal, vAC);
normals[triangleCount] = normal;
triangles[triangleCount] =  Clazz.newIntArray (-1, [isWindingOK ? i : j, isWindingOK ? j : i, k, -7]);
if (!this.checkFace (points, vertexCount, triangles, normals, triangleCount, pTemp, nTemp, vAC, htNormMap, htEdgeMap, planarParam, bsTemp)) continue;
if (isThroughCenter) {
bsCenterPlanes.set (triangleCount++);
} else if (collapsed) {
ptRef.setT (points[nPoints] =  new JU.P3 ());
points[nPoints].scaleAdd2 (offset, normal, centralAtom);
this.addFacet (i, j, k, ptRef, points, normals, triangles, triangleCount++, nPoints, isWindingOK, vAC);
this.addFacet (k, i, j, ptRef, points, normals, triangles, triangleCount++, nPoints, isWindingOK, vAC);
this.addFacet (j, k, i, ptRef, points, normals, triangles, triangleCount++, nPoints, isWindingOK, vAC);
nPoints++;
} else {
triangleCount++;
}}
}

nPoints--;
if (JU.Logger.debugging) {
JU.Logger.info ("Polyhedron planeCount=" + triangleCount + " nPoints=" + nPoints);
for (var i = 0; i < triangleCount; i++) JU.Logger.info ("Polyhedron " + JU.PT.toJSON ("face[" + i + "]", triangles[i]));

}return  new J.shapespecial.Polyhedron ().set (centralAtom, points, nPoints, vertexCount, triangles, triangleCount, this.getFaces (triangles, triangleCount, htNormMap), normals, bsCenterPlanes, collapsed, this.distanceRef);
}, "JM.Atom,~N");
Clazz.defineMethod (c$, "addFacet", 
 function (i, j, k, ptRef, points, normals, faces, planeCount, nRef, isWindingOK, vTemp) {
var normal =  new JU.V3 ();
JU.Measure.getNormalFromCenter (points[k], ptRef, points[i], points[j], false, normal, vTemp);
normals[planeCount] = normal;
faces[planeCount] =  Clazz.newIntArray (-1, [nRef, isWindingOK ? i : j, isWindingOK ? j : i, -2]);
}, "~N,~N,~N,JU.P3,~A,~A,~A,~N,~N,~B,JU.V3");
Clazz.defineMethod (c$, "checkFace", 
 function (points, nPoints, triangles, normals, index, pTemp, vNorm, vAC, htNormMap, htEdgeMap, planarParam, bsTemp) {
var p1 = triangles[index];
var i0 = p1[0];
pTemp = JU.Measure.getPlaneThroughPoints (points[i0], points[p1[1]], points[p1[2]], vNorm, vAC, pTemp);
var pt = points[i0];
for (var j = 0; j < nPoints; j++) {
if (j == i0) continue;
vAC.sub2 (points[j], pt);
vAC.normalize ();
var v = vAC.dot (vNorm);
if (v > 0.02) {
return false;
}}
var norm = normals[index];
var normix = Integer.$valueOf (JU.Normix.getNormixV (norm, bsTemp));
var o = htNormMap.get (normix);
if (o == null) {
var norms = JU.Normix.getVertexVectors ();
for (var e, $e = htNormMap.entrySet ().iterator (); $e.hasNext () && ((e = $e.next ()) || true);) {
var n = e.getKey ();
if (norms[n.intValue ()].dot (norm) > planarParam) {
normix = n;
o = e.getValue ();
break;
}}
if (o == null) htNormMap.put (normix, o =  Clazz.newArray (-1, [ new JU.BS (),  new JU.Lst ()]));
}var bsPts = o[0];
var lst = o[1];
for (var i = 0; i < 3; i++) if (!this.addEdge (lst, htEdgeMap, normix, p1, i, points, bsPts)) return false;

return true;
}, "~A,~N,~A,~A,~N,JU.P4,JU.V3,JU.V3,java.util.Map,java.util.Map,~N,JU.BS");
Clazz.defineMethod (c$, "addEdge", 
 function (faceList, htEdgeMap, normix, p1, i, points, bsPts) {
var pt1 = p1[(i + 1) % 3];
var s1 = "_" + pt1;
var pt = p1[i];
var s = "_" + pt;
var edge = normix + s + s1;
if (htEdgeMap.containsKey (edge)) return false;
var edge0 = normix + s1 + s;
var o = htEdgeMap.get (edge0);
var b;
if (o == null) {
var coord2 = points[pt1];
var coord1 = points[pt];
this.vAB.sub2 (coord2, coord1);
for (var j = bsPts.nextSetBit (0); j >= 0; j = bsPts.nextSetBit (j + 1)) {
if (j == pt1 || j == pt) continue;
this.vAC.sub2 (points[j], coord1);
if (o == null) {
o = bsPts;
this.vBC.cross (this.vAC, this.vAB);
continue;
}this.vAC.cross (this.vAC, this.vAB);
if (this.vBC.dot (this.vAC) < 0) return false;
}
bsPts.set (pt);
bsPts.set (pt1);
b =  Clazz.newIntArray (-1, [pt, pt1]);
faceList.addLast (b);
htEdgeMap.put (edge,  Clazz.newArray (-1, [p1, Integer.$valueOf (i), b]));
} else {
var p10 = (o)[0];
if (p10 == null) return false;
var i0 = ((o)[1]).intValue ();
p10[3] = -((-p10[3]) ^ (1 << i0));
p1[3] = -((-p1[3]) ^ (1 << i));
b = (o)[2];
for (var j = faceList.size (); --j >= 0; ) {
var f = faceList.get (j);
if (f[0] == b[0] && f[1] == b[1]) {
faceList.remove (j);
break;
}}
htEdgeMap.put (edge,  Clazz.newArray (-1, [null]));
htEdgeMap.put (edge0,  Clazz.newArray (-1, [null]));
}return true;
}, "JU.Lst,java.util.Map,Integer,~A,~N,~A,JU.BS");
Clazz.defineMethod (c$, "isPlanar", 
 function (pt1, pt2, pt3, ptX) {
var norm =  new JU.V3 ();
var w = JU.Measure.getNormalThroughPoints (pt1, pt2, pt3, norm, this.vAB);
var d = JU.Measure.distanceToPlaneV (norm, w, ptX);
return (Math.abs (d) < J.shapespecial.Polyhedra.MAX_DISTANCE_TO_PLANE);
}, "JU.P3,JU.P3,JU.P3,JU.P3");
Clazz.defineMethod (c$, "getFaces", 
 function (triangles, triangleCount, htNormMap) {
var n = htNormMap.size ();
var faces = JU.AU.newInt2 (n);
if (triangleCount == n) {
for (var i = triangleCount; --i >= 0; ) faces[i] = JU.AU.arrayCopyI (triangles[i], 3);

return faces;
}var fpt = 0;
for (var e, $e = htNormMap.entrySet ().iterator (); $e.hasNext () && ((e = $e.next ()) || true);) {
var faceList = e.getValue ()[1];
n = faceList.size ();
var face = faces[fpt++] =  Clazz.newIntArray (n, 0);
if (n < 2) continue;
var edge = faceList.get (0);
face[0] = edge[0];
face[1] = edge[1];
var pt = 2;
var i0 = 1;
var pt0 = -1;
while (pt < n && pt0 != pt) {
pt0 = pt;
for (var i = i0; i < n; i++) {
edge = faceList.get (i);
if (edge[0] == face[pt - 1]) {
face[pt++] = edge[1];
if (i == i0) i0++;
break;
}}
}
}
return faces;
}, "~A,~N,java.util.Map");
Clazz.overrideMethod (c$, "setModelVisibilityFlags", 
function (bsModels) {
for (var i = this.polyhedronCount; --i >= 0; ) {
var p = this.polyhedrons[i];
if (this.ms.at[p.centralAtom.i].isDeleted ()) p.isValid = false;
p.visibilityFlags = (p.visible && bsModels.get (p.centralAtom.mi) && !this.ms.isAtomHidden (p.centralAtom.i) && !this.ms.at[p.centralAtom.i].isDeleted () ? this.vf : 0);
if (p.visibilityFlags != 0) this.setShapeVisibility (this.atoms[p.centralAtom.i], true);
}
}, "JU.BS");
Clazz.overrideMethod (c$, "getShapeState", 
function () {
if (this.polyhedronCount == 0) return "";
var s =  new JU.SB ();
for (var i = 0; i < this.polyhedronCount; i++) if (this.polyhedrons[i].isValid) s.append (this.polyhedrons[i].getState (this.vwr));

if (this.drawEdges == 2) J.shape.Shape.appendCmd (s, "polyhedra frontedges");
 else if (this.drawEdges == 1) J.shape.Shape.appendCmd (s, "polyhedra edges");
s.append (this.vwr.getAtomShapeState (this));
for (var i = 0; i < this.polyhedronCount; i++) {
var p = this.polyhedrons[i];
if (p.isValid && p.colixEdge != 0 && this.bsColixSet.get (p.centralAtom.i)) J.shape.Shape.appendCmd (s, "select ({" + p.centralAtom.i + "}); color polyhedra " + (JU.C.isColixTranslucent (this.colixes[p.centralAtom.i]) ? "translucent " : "") + JU.C.getHexCode (this.colixes[p.centralAtom.i]) + " " + JU.C.getHexCode (p.colixEdge));
}
return s.toString ();
});
Clazz.defineStatics (c$,
"DEFAULT_FACECENTEROFFSET", 0.25,
"EDGES_NONE", 0,
"EDGES_ALL", 1,
"EDGES_FRONT", 2,
"MAX_VERTICES", 250,
"FACE_COUNT_MAX", 247);
c$.randomPoint = c$.prototype.randomPoint = JU.P3.new3 (3141, 2718, 1414);
Clazz.defineStatics (c$,
"MODE_BONDING", 1,
"MODE_POINTS", 2,
"MODE_RADIUS", 3,
"MODE_BITSET", 4,
"MODE_UNITCELL", 5,
"MODE_INFO", 6,
"DEFAULT_PLANAR_PARAM", 0.98,
"CONVEX_HULL_MAX", 0.02,
"MAX_DISTANCE_TO_PLANE", 0.1);
});
