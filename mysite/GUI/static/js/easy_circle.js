// progressbar.js@1.0.0 version is used
// Docs: http://progressbarjs.readthedocs.org/en/1.0.0/

var bar = new ProgressBar.Circle(container, {
  strokeWidth: 20,
  easing: 'easeInOut',
  duration: 1400,
  color: '#6dc066',
  trailColor: '#eee',
  trailWidth: 1,
  svgStyle: null
});

bar.animate(0.77);  // Number from 0.0 to 1.0