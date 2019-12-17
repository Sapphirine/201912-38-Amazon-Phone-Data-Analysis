function getReviewConfidence(){
    var product = $("#product_box option:selected").text()
    console.log("confience")
    console.log(product)

    $.ajax({
        type: 'POST',
        url: "/get_confidence",
        data: JSON.stringify({'product': product}),
        contentType: 'application/json;charset=UTF-8',
        success: function(response){
             $("#my_div").empty();
            // set the dimensions and margins of the graph
            var width = 700
                height = 700
                margin = 40

            // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
            var radius = Math.min(width, height) / 2 - margin

            // append the svg object to the div called 'my_dataviz'
            var svg = d3.select("#my_div")
              .append("svg")
                .attr("width", width)
                .attr("height", height)
              .append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
            var aa = response['result']['confidence'] * 100
            // Create dummy data
            var data = {a: {"name":"untrusted", "num": 100-aa}, b:  {"name":"trusted", "num": aa}}

            // set the color scale
            var color = d3.scaleOrdinal()
              .domain(["a", "b"])
              .range(d3.schemeDark2);

            // Compute the position of each group on the pie:
            var pie = d3.pie()
              .sort(null) // Do not sort group by size
              .value(function(d) { return d.value.num; })
            var data_ready = pie(d3.entries(data))

            // The arc generator
            var arc = d3.arc()
              .innerRadius(radius * 0.5)         // This is the size of the donut hole
              .outerRadius(radius * 0.8)

            // Another arc that won't be drawn. Just for labels positioning
            var outerArc = d3.arc()
              .innerRadius(radius * 0.9)
              .outerRadius(radius * 0.9)

            // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
            svg
              .selectAll('allSlices')
              .data(data_ready)
              .enter()
              .append('path')
              .attr('d', arc)
              .attr('fill', function(d){ return(color(d.data.key)) })
              .attr("stroke", "white")
              .style("stroke-width", "2px")
              .style("opacity", 0.9)

            svg
              .selectAll('allLabels')
              .data(data_ready)
              .enter()
              .append('text')
                .text( function(d) { console.log(d.data.value.name);  return d.data.value.name } )
                .attr('transform', function(d) {
                    var pos = outerArc.centroid(d);
                    var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                    pos[0] = radius * 0.8 * (midangle < Math.PI ? 1 : -1);
                    return 'translate(' + pos + ')';
                })
                .style('text-anchor', function(d) {
                    var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                    return (midangle < Math.PI ? 'start' : 'end')
                })
        }
    })

}