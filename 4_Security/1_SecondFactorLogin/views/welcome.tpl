% include('header.tpl')

<div class="connection-box-wrap">
    <div class="connection-box">

        <h1>Welcome {{ user['name'] }}!!!</h1>

        <a href="/change_password" class="form-input-change" style="width:200px;">Change password</a>

    </div>
</div>

% include('footer.tpl')