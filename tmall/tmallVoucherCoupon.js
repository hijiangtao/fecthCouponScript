//@hijiangtao
//Page: https://www.tmall.com/wow/act/14700/pre20151111

var getVoucherBtn = function () {
	var judEff = 0;
	setInterval(function() {
        var close = document.querySelector('#voucherBtn');
        if (close != null) {
        	var re = new RegExp();  
			re = new RegExp("本时段已抢完");
			//console.log(re);
        	if (!re.test(close.innerText))
        		judEff = 1;
        	else
        		judEff = 0;

        	if (judEff) {
        		close.click();
        	}
        	else {
        		alert('购物券可能已经发完，现在刷新页面，请在页面刷新后重新复制代码运行！')
        		window.location.reload();
        	}
        }
    }, 500);
}

getVoucherBtn();