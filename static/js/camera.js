var flag = false;
var mode;

function addCamera(evt) {
	if (mode != "addCamera") {
		return false;
	}
	var camera=document.createElementNS("http://www.w3.org/2000/svg", "g");
	//camera.className="camera";
	//camera.classList.add("camera");	
	camera.setAttribute("class","camera");
	this.appendChild(camera);

	var cameraLense = document.createElementNS("http://www.w3.org/2000/svg", "use");
	cameraLense.setAttribute("class","cameraLense");
	//如果仅仅用camera.setAttribute("xlink:href","#camera")不会起作用，因为未引入命名空间
	cameraLense.setAttributeNS("http://www.w3.org/1999/xlink", "href", "#cameraLense");
	camera.appendChild(cameraLense);

	var cameraNo = document.createElementNS("http://www.w3.org/2000/svg", "text");
	camera.appendChild(cameraNo);
	cameraNo.style.setProperty("text-anchor", "middle");
	
	var oStyle =window.getComputedStyle(cameraNo,null);
	//var text_offset=parseInt(cameraNo.style.getPropertyValue("font-size"))*0.4;
	var text_offset=parseInt(oStyle.getPropertyValue("font-size"))*0.4;
	console.log("text_offset"+text_offset);
	cameraNo.setAttribute("y", text_offset);
	//text默认以基线对齐
	cameraNo.style.setProperty("text-anchor", "middle");
	var textString = document.createTextNode(document.querySelectorAll(".camera").length);
	cameraNo.appendChild(textString);

	
	var pt = convertPt(this, evt.clientX, evt.clientY);
	var x=pt.x;
	var y=pt.y;
	camera.initX=x;
	camera.initY=y;
	camera.initTheta=0;    
    camera.currentX=camera.initX;
    camera.currentY=camera.initY;
    camera.currentTheta=camera.initTheta;
 	for (var i = camera.childNodes.length - 1; i >= 0; i--) {
 		var obj=camera.childNodes[i]
		obj.initX=x;
		obj.initY=y;   
	    obj.currentX=obj.initX;
	    obj.currentY=obj.initY;
	}	
	var transformBaseVal = camera.transform.baseVal;
	if (transformBaseVal.numberOfItems == 0) {
		var transformObject = svgRoot.createSVGTransform();
		transformBaseVal.appendItem(transformObject);
	}
	var transformItem = transformBaseVal.getItem(0);
	transformItem.setTranslate(x, y);
	console.log("----initial Camera:initX="+camera.initX+",initY="+camera.initX+"----");
}

function removeCamera(evt,mode) {
	if (mode != "delCamera") {
		return false;
	}
	console.log("----remove begin----");
	var obj = evt.target;
	var objParent=obj.parentNode;
	if (objParent.getAttribute("class")!="camera") {return false;}
	svgRoot.removeChild(objParent);
	console.log("----remove end----");
}

var startX, startY, startTheta;

function mousedown(evt,mode) {
	console.log("mode=" + mode);
	if (mode != "rotateCamera" && mode != "dragCamera") {
		return false;
	}
	var obj = evt.target;
	var objParent=obj.parentNode;
	if(objParent.getAttribute("class")!="camera"){
		return false;
	}
	objParent.initX=objParent.currentX;
	objParent.initY=objParent.currentY;
	objParent.initTheta=objParent.currentTheta;
	for (var i = objParent.childNodes.length - 1; i >= 0; i--) {
		var objSibbing=objParent.childNodes[i];
		objSibbing.initX=objSibbing.currentX;
		objSibbing.initY=objSibbing.currentY;
	}
	
	var pt = convertPt(svgRoot, evt.clientX, evt.clientY);
	startX = pt.x;
	startY = pt.y;
	startTheta = Math.atan2(startY - objParent.initY, startX - objParent.initX) * 180 / Math.PI;
	console.log("hit me! Theta=" + parseInt(objParent.initTheta) + ",x=" + objParent.initX + ",y=" + objParent.initY);
	flag = true;
}

function rotate(evt,mode) {
	if (mode != "rotateCamera" || !flag) {
		return false;
	}

	var obj = evt.target;
	var objParent=obj.parentNode;

	if(obj.getAttribute("class")!="cameraLense"){
		return false;
	}
	console.log("----start rotate----");
	var pt = convertPt(svgRoot, evt.clientX, evt.clientY);
	var endX = pt.x;
	var endY = pt.y;
	var endTheta = Math.atan2(endY - objParent.initY, endX - objParent.initX) * 180 / Math.PI;
	var deltaTheta = endTheta - startTheta;
	objParent.currentTheta = objParent.initTheta + deltaTheta;

	var transformBaseVal = obj.transform.baseVal;
	if (transformBaseVal.numberOfItems == 0) {
		var transformObject = svgRoot.createSVGTransform();
		transformBaseVal.appendItem(transformObject);
	}
	var transformItem = transformBaseVal.getItem(0);
	transformItem.setRotate(objParent.currentTheta,0,0);

	obj.style.cursor = "default";
	console.log(obj.getAttribute("transform"));
	console.log("----end rotate----");
}

function drag(evt,mode) {
	if (mode != "dragCamera" || !flag) {
		return false;
	}
	var obj = evt.target;
	var objParent=obj.parentNode;
	if(objParent.getAttribute("class")!="camera"){
		return false;
	}

	console.log("----start drag----");	
	var pt = convertPt(svgRoot, evt.clientX, evt.clientY);
	var deltaX = pt.x - startX;
	var deltaY = pt.y - startY;
	if (obj.getAttribute("class")=="cameraLense") {
		objParent.currentX=parseInt(objParent.initX + deltaX);
		objParent.currentY=parseInt(objParent.initY+ deltaY);
		for (var i = objParent.childNodes.length - 1; i >= 0; i--) {
			var objSibbing=objParent.childNodes[i];
			objSibbing.currentX=parseInt(objSibbing.initX + deltaX);
			objSibbing.currentY=parseInt(objSibbing.initY+ deltaY);
		}

		var transformBaseVal = objParent.transform.baseVal;
		if (transformBaseVal.numberOfItems == 0) {
			var transformObject = svgRoot.createSVGTransform();
			transformBaseVal.appendItem(transformObject);
		}
		var transformItem = transformBaseVal.getItem(0);
		transformItem.setTranslate(objParent.currentX, objParent.currentY);

	} else if(obj.nodeName.toLowerCase()=="image"&&obj.parentNode.getAttribute("class")=="camera"){
		obj.currentX=parseInt(obj.initX + deltaX);
		obj.currentY=parseInt(obj.initY+ deltaY);
		var transformBaseVal = obj.transform.baseVal;
		if (transformBaseVal.numberOfItems == 0) {
			var transformObject = svgRoot.createSVGTransform();
			transformBaseVal.appendItem(transformObject);
		}
		var transformItem = transformBaseVal.getItem(0);
		transformItem.setTranslate(deltaX, deltaY);
	}

	obj.style.cursor = "move";
	console.log(obj.getAttribute("transform"));
	console.log("----end drag----");
}

function mouseup(evt,mode) {
	flag = false;
	console.log("release me!");
}

function convertPt(svgRoot, x, y) {
	var svgPoint = svgRoot.createSVGPoint();
	var im = svgRoot.getScreenCTM().inverse(); // inverse of tranforma matrix         
	// set point with window coordination
	svgPoint.x = x;
	svgPoint.y = y;
	// convert point to SVG coordination
	var pt = svgPoint.matrixTransform(im);
	return pt;
}