// Incremental reveal: elements with class "step" inside a slide appear one per
// Next press. Prev hides them again before leaving the slide. Loaded from a
// slide file (not index.html) so slyds commands and `slyds update` leave it be.
(function () {
    if (window.slydsSteps) return;
    window.slydsSteps = true;

    function steps() {
        var slide = document.querySelector('.slide.active');
        return slide ? slide.querySelectorAll('.step') : [];
    }

    // Returns true if the press was consumed by a step.
    function advance(dir) {
        var s = steps();
        if (dir > 0) {
            for (var i = 0; i < s.length; i++) {
                if (!s[i].classList.contains('shown')) { s[i].classList.add('shown'); return true; }
            }
        } else {
            for (var j = s.length - 1; j >= 0; j--) {
                if (s[j].classList.contains('shown')) { s[j].classList.remove('shown'); return true; }
            }
        }
        return false;
    }

    // Entering going forward starts with nothing shown; going back shows everything.
    document.addEventListener('slideEnter', function (e) {
        var back = e.detail && e.detail.direction === 'backward';
        e.target.querySelectorAll('.step').forEach(function (el) { el.classList.toggle('shown', back); });
    });

    // slyds.js defines changeSlide after the slides are parsed, so wrap it once the DOM is ready.
    document.addEventListener('DOMContentLoaded', function () {
        var engineChange = window.changeSlide;
        window.changeSlide = function (n) { if (!advance(n)) engineChange(n); };
    });

    // Capture phase so we see the arrow keys before slyds.js's own handler.
    document.addEventListener('keydown', function (e) {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        e.stopImmediatePropagation();
        window.changeSlide(e.key === 'ArrowRight' ? 1 : -1);
    }, true);
})();
