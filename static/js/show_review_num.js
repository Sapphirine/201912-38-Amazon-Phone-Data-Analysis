function getReviewNum(){
    var product = $("#product_box option:selected").text()

    $.ajax({
        type: 'POST',
        url: "/get_review_num",
        data: JSON.stringify({'product': product}),
        contentType: 'application/json;charset=UTF-8',
        success: function(response){
            $("#my_div").empty();
            var dataset = response['result'];
//            console.log("this is rating list")
//            console.log(rating_list);
            // 2. Use the margin convention practice
            var margin = {top: 50, right: 50, bottom: 50, left: 50}
              , width = document.body.clientWidth/2 - margin.left - margin.right // Use the window's width
              , height = document.body.clientHeight/2 - margin.top - margin.bottom; // Use the window's height

            // The number of datapoints
            var n = 5;

            // 5. X scale will use the index of our data
            var xScale = d3.scaleLinear()
                .domain([0, n]) // input
                .rangeRound([0, width]); // output

            // 6. Y scale will use the randomly generate number
            var yScale = d3.scaleLinear()
                .domain([0, 20]) // input
                .range([height, 0]); // output

            // 7. d3's line generator
            var line = d3.line()
                .x(function(d, i) { return xScale(d.rating); }) // set the x values for the line generator
                .y(function(d) { return yScale(d.num); }) // set the y values for the line generator
                .curve(d3.curveMonotoneX) // apply smoothing to the line

            // 8. An array of objects of length N. Each object has key -> value pair, the key being "y" and the value is a random number
//            var dataset = d3.range(n+1).map(function(d, i) { return {"rating": i, "num": d3.randomUniform(1)() } })
            console.log(dataset)


            // 1. Add the SVG to the page and employ #2
            var svg = d3.select("#my_div").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            // 3. Call the x axis in a group tag
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

            // 4. Call the y axis in a group tag
            svg.append("g")
                .attr("class", "y axis")
                .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

            // 9. Append the path, bind the data, and call the line generator
            svg.append("path")
                .datum(dataset) // 10. Binds data to the line
                .attr("class", "line") // Assign a class for styling
                .attr("d", line); // 11. Calls the line generator

            // 12. Appends a circle for each datapoint
            svg.selectAll(".dot")
                .data(dataset)
              .enter().append("circle") // Uses the enter().append() method
                .attr("class", "dot") // Assign a class for styling
                .attr("cx", function(d) { return xScale(d.rating) })
                .attr("cy", function(d) { return yScale(d.num) })
                .attr("r", 5)
                  .on("mouseover", function(a, b, c) {
                        console.log(a)
                    this.attr('class', 'focus')
                    })
                  .on("mouseout", function() {  })
            // text label for the x axis
            svg.append("text")             
                .attr("y", width/2)
                .attr("x",height)
                .style("text-anchor", "middle")
                .text("Ratings");

            // text label for the y axis
            svg.append("text")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 0 - 50)
                  .attr("x",0 - (height / 2))
                  .attr("dy", "1em")
                  .style("text-anchor", "middle")
                  .text("Number of reviews");      
        }
    })
}