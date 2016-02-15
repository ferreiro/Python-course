% include('header.tpl')

<h1>
	Change email for a username
</h1>

<form action="/change_email" method="POST">

	<div class="input">
		<p>Username</p>
		<input name="_id" type="text" value="" placeholder="Username" />
	</div>

	<div class="input">
		<p>New email</p>
		<input name="email" type="text" value="" placeholder="New email" />
	</div>

	<input type="submit" value="Send me!">
</form>

% include('footer.tpl')