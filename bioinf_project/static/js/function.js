// JavaScript Document

function tabSwitch(new_tab, new_content) {
	
	document.getElementById('content_1').style.display = 'none';
	document.getElementById('content_2').style.display = 'none';
	document.getElementById('content_3').style.display = 'none';		
	document.getElementById(new_content).style.display = 'block';	
	

	document.getElementById('tab_1').className = '';
	document.getElementById('tab_2').className = '';
	document.getElementById('tab_3').className = '';		
	document.getElementById(new_tab).className = 'active';		

}

// Ties a set of tabs and content id's together, and switches between them
// <div id='tab_1'> and <div id="content_1"> for example
// Usage: tabswitch(1, 4, 'tab', 'panel') would switch on tab_1 and panel_1

function tabSwitch_2(active, number, tab_prefix, content_prefix) {
	
	for (var i=1; i < number+1; i++) {
	  document.getElementById(content_prefix+i).style.display = 'none';
	  document.getElementById(tab_prefix+i).className = '';
	}
	document.getElementById(content_prefix+active).style.display = 'block';
	document.getElementById(tab_prefix+active).className = 'active';	
	
}