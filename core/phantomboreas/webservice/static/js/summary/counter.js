var Counter = function(number, container) {
    this.container = container;
    this.number = number;
}

Counter.prototype.render = function() {
    var stringVal = this.number.toString(),
        arr = stringVal.split('');

    for(var i = 0; i < arr.length; i++) {
        this.container.append("<span class='number'>"+arr[i]+"</span>");

        if((arr.length - i - 1) % 3 === 0 && (arr.length - i - 1) !== 0) {
            this.container.append("<span class='comma'>,</span>");
        }
    }
}