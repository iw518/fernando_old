class SvgContainer {

    constructor(parentId, id = "svgContainer", width = 600, height = 400, scaleX = 1, scaleY = -1, boxWidth = 900, boxHeight = 600) {
        this.svgns = "http://www.w3.org/2000/svg";
        this.offsetX = boxWidth / 10;
        this.offsetY = boxHeight / 10;
        this.svg = document.createElementNS(this.svgns, "svg");
        $("#" + parentId).append(this.svg);
        this.svg.setAttribute("version", "1.1");
        this.svg.setAttribute("xmlns", this.svgns);
        this.svgDoc = this.svg.ownerDocument;
        this.id = id;
        this.width = width;
        this.height = height;
        this.scaleX = scaleX;
        this.scaleY = scaleY;
        this.boxWidth = boxWidth;
        this.boxHeight = boxHeight;
        this.minX = 0;
        this.minY = this.boxHeight * this.scaleY;
        this.svg.setAttribute("id", id);
        this.svg.style.setProperty("width", this.width);
        this.svg.style.setProperty("height", this.height);
        var boxValue = this.minX + " " + this.minY + " " + this.boxWidth + " " + this.boxHeight;
        //注意viewBox 大小写敏感
        this.svg.setAttribute("viewBox", boxValue);
        this.diagram = this.svgDoc.createElementNS(this.svgns, "g");
        this.svg.appendChild(this.diagram);
        var scale = "scale(" + this.scaleX + "," + this.scaleY + ")";
        var translate = "translate(" + this.offsetX + "," + this.offsetY + ")";
        this.diagram.setAttribute("transform", scale + " " + translate);
    }

    creatAxis(yTitle = "Y Title") {
        //定义marker
        let defs = this.svgDoc.createElementNS(this.svgns, "defs");
        let marker = this.svgDoc.createElementNS(this.svgns, "marker");
        marker.setAttribute("id", "arrow");
        //特别注意marker显示的高宽，否则很有可能只显示一半
        marker.setAttribute("markerWidth", 12);
        marker.setAttribute("markerHeight", 12);
        marker.setAttribute("refX", 0);
        marker.setAttribute("refY", 4);
        marker.setAttribute("orient", "auto");
        marker.setAttribute("markerUnits", "strokeWidth");
        let path = this.svgDoc.createElementNS(this.svgns, "path");
        path.setAttribute("stroke", "none");
        path.setAttribute("fill", "red");
        let d = "M 0 0 12 4 0 8 Z";
        path.setAttribute("d", d);
        marker.appendChild(path);
        defs.appendChild(marker);
        this.svg.appendChild(defs);
        //生成axis
        var axis = this.svgDoc.createElementNS(this.svgns, "g");
        axis.setAttribute("id", "axis");
        axis.style.setProperty("stroke", "black");
        var axisX = this.svgDoc.createElementNS(this.svgns, "line");
        axisX.setAttribute("x1", 0);
        axisX.setAttribute("y1", 0);
        axisX.setAttribute("x2", this.boxWidth * 0.8);
        axisX.setAttribute("y2", axisX.getAttribute("y1"));
        axisX.style.setProperty("stroke-width", 2);
        axis.appendChild(axisX);
        var axisY = this.svgDoc.createElementNS(this.svgns, "line");
        axisY.setAttribute("x1", 0);
        axisY.setAttribute("y1", 0);
        axisY.setAttribute("x2", axisY.getAttribute("x1"));
        axisY.setAttribute("y2", this.boxHeight * 0.8);
        axisY.style.setProperty("stroke-width", 2);
        axis.appendChild(axisY);
        axisX.setAttribute("marker-end", "url(#arrow)");
        axisY.setAttribute("marker-end", "url(#arrow)");
        this.diagram.appendChild(axis);

        var groupCircle = this.svgDoc.createElementNS(this.svgns, "g");
        groupCircle.setAttribute("id", "groupCircle");
        var txt = this.svgDoc.createElementNS(this.svgns, "text");
        txt.style.setProperty("fill", "blue");
        txt.setAttribute("id", "circle_note");
        groupCircle.appendChild(txt);
        this.diagram.appendChild(groupCircle);
    }

    show(data, unit, xWidth, yHeight) {
        var groupCircle = this.svgDoc.getElementById("groupCircle");
        var rings = groupCircle.getElementsByTagName("circle");
        var n = rings.length;
        for (var i = n - 1; i >= 0; i--) {
            groupCircle.removeChild(rings[i]);
        }
        for (var i = 0; i < data.length; i++) {
            var item = data[i];
            if ($("#layerNo").find("option:selected").text() == item[0]) {
                var max = -10000;
                var min = 10000;
                var maxobj;
                var minobj;
                for (var j = 0; j < item[1].length; j++) {

                    var childitem = item[1][j];
                    var name = childitem[0];
                    var value = childitem[1];
                    var r = 4;
                    var circle = this.svgDoc.createElementNS(this.svgns, "circle");
                    circle.setAttribute("id", name);
                    circle.setAttribute("cx", (j + 1) / (item[1].length) * (xWidth - 50));
                    circle.setAttribute("cy", value * yHeight / 10);
                    circle.setAttribute("value", value);
                    circle.setAttribute("r", r);
                    circle.style.setProperty("fill-opacity", 0.5);
                    circle.addEventListener("click", function(evt) {
                        grow(evt, "circle_note", unit);
                    }); //注意参数调用方式
                    circle.addEventListener("mouseout", function(evt) {
                        shrink(evt, "circle_note");
                    });

                    var grow_animate = this.svgDoc.createElementNS(this.svgns, "animate");
                    var beginEvt = circle.getAttribute("id") + ".click";
                    grow_animate.setAttribute("begin", beginEvt);
                    grow_animate.setAttribute("attributeName", "r");
                    grow_animate.setAttribute("values", r + ";" + 4 * r + ";" + r); //"4;16;4"
                    grow_animate.setAttribute("dur", "2s");
                    grow_animate.setAttribute("fill", "freeze");
                    circle.appendChild(grow_animate);

                    if (max < value) {
                        max = value;
                        maxobj = circle;
                    }
                    if (min > value) {
                        min = value;
                        minobj = circle;
                    }
                    groupCircle.appendChild(circle);
                }
                this.limitAnimation(maxobj, "red");
                this.limitAnimation(minobj, "blue");
            }
        }
    }

    //最大值，最小值双闪
    limitAnimation(obj, stroke_color) {
        var groupCircle = document.getElementById("groupCircle");
        var r = obj.getAttribute("r");
        var x = obj.getAttribute("cx");
        var y = obj.getAttribute("cy");
        var circle = this.svgDoc.createElementNS(this.svgns, "circle");
        groupCircle.appendChild(circle);
        circle.setAttribute("r", 2 * r);
        circle.setAttribute("cx", x);
        circle.setAttribute("cy", y);
        circle.style.setProperty("stroke-width", "4");
        circle.style.setProperty("stroke", stroke_color);
        circle.style.setProperty("fill", "none");

        var animate = document.createElementNS(this.svgns, "animate");
        circle.appendChild(animate);
        animate.setAttribute("attributeName", "stroke-opacity");
        animate.setAttribute("values", "1;0;1");
        animate.setAttribute("begin", "0s");
        animate.setAttribute("dur", "4s");
        animate.setAttribute("repeatCount", "indefinite");
    }
}

function grow(evt, id, unit) {
    var obj = evt.target;
    obj.style.setProperty("fill", "red");
    var x = obj.getAttribute("cx");
    var y = obj.getAttribute("cy");
    var name = obj.getAttribute("id");
    var value = obj.getAttribute("value");
    var txt = document.getElementById(id);

    txt.style.setProperty("font-size", "20px");
    txt.setAttribute("x", x);
    txt.setAttribute("y", y);
    txt.setAttribute("transform", "translate(0," + y * 2 + ") scale(1,-1)");
    if (txt.childNodes.length == 0) {
        txt.appendChild(document.createTextNode(""));
    }
    txt.firstChild.data = name + "对应" + (value / 1.0).toFixed(2) + unit;
    console.log(obj.childNodes);
}

function shrink(evt, id) {
    var obj = evt.target;
    obj.setAttribute("r", 4);
    obj.style.setProperty("fill", "black");
    var txt = document.getElementById(id);
    if (txt.childNodes.length > 0) {
        txt.firstChild.data = "";
    }
}