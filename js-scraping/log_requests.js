XMLHttpRequest.prototype.nativeOpen = XMLHttpRequest.prototype.open;

XMLHttpRequest.prototype.customOpen = function(method, url, asynch, user, password)
{
    console.log(method, url, asynch, user, password);
    return this.nativeOpen(method, url, asynch, user, password);
};

XMLHttpRequest.prototype.open = XMLHttpRequest.prototype.customOpen;