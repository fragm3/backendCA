def send_reset_link_html(name,link):
    html = '<html><head>'
    html = html + '</head>'
    html = html + '<body style="font-family: Arial; font-size: 12px;">'
    html = html + '<div>'
    html = html + 'Hi' + name + ',<br>'
    html = html + '<p>Someone requested a password reset for your email ID. No changes have been done yet.' \
           ' Please follow the link below to reset your password.</p>'
    html = html + '<p>'
    html = html + '<a href="'+ link +'">Follow this link to reset your password.</a>'
    html = html + '</div></body></html>'
    return html

