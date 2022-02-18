$(document).ready(function(){
    $('.slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: false,
        arrows: false,
    });
     go_news(0);
});

function go_news(news_position, stop) {
    bars = document.getElementsByClassName("bar")
    var ProgressBar = {
        target: bars[news_position],
        widthIncrement: 0.8,
        width: 0,
        id: null,
        reset: function() {
            this.width = 0;
        },
        move: function() {
            var self = ProgressBar;
            self.id = window.requestAnimationFrame(self.move);
            self.width += self.widthIncrement;
            self.target.style.width = self.width + "%";
            if (self.width >= 100) {
                self.stop();
                $('.slider').slick('slickNext');
            }
        },
        stop: function() {
            window.cancelAnimationFrame(this.id);
        }
    }
    if (stop == true) {
        ProgressBar.stop()
    } else {
        ProgressBar.move()
    };
};


$('.slider').on('beforeChange', function(event, slick, currentSlide, nextSlide){
    bars = document.getElementsByClassName("bar")
    if (nextSlide == 0) {
        go_news(currentSlide, true)
        for (i=0; i<bars.length; i++) {
            bars[i].style.width = '0%'
            if (i == bars.length-1) {console.log(true)};
        };
    };
    go_news(nextSlide, false)
});


$('.slider').on('swipe', function(slick, direction){
    current = direction.currentSlide
    direct = direction.currentDirection
    console.log(direction)
});