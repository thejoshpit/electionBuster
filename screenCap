// How to: save as capture.js and run with "phantomjs capture.js"
// Setup by modifying URLS, PAGE_WIDTH AND PAGE_HEIGHT constants!
// Hint: set PAGE_WIDTH or PAGE_HEIGHT to 0 to capture full page!
// Requires Phantom JS
// modified version of script at http://www.cameronjtinker.com/post/2011/09/26/Take-Screenshot-of-all-HTML-documents-in-a-folder-using-PhantomJS.aspx
// 
var PAGE_WIDTH = 0;
var PAGE_HEIGHT = 0;

var URLS = [
"http://www.testURL1.com",
"http://www.testURL2.com",
];

// phantomjs page object and helper flag
var page = require('webpage').create(),
  loadInProgress = false,
  pageIndex = 0;


// set clip and viewport based on PAGE_WIDTH and PAGE_HEIGHT constants
if (PAGE_WIDTH > 0 && PAGE_HEIGHT > 0) {
  page.viewportSize = {
    width: PAGE_WIDTH,
    height: PAGE_HEIGHT
  };

  page.clipRect = {
    top: 0,
    left: 0,
    width: PAGE_WIDTH,
    height: PAGE_HEIGHT
  };
}
