% include('header.tpl')

<h1>
	Edit @{{user['_id']}} email
</h1>

<form action="/change_email" method="POST">

	% for key in user:
		<div class="input">

			<legend id="{{ key }}">
				{{ key }}
			</legend>

			% if key == "email":
				<input name="{{ key }}" type="text" value="{{user[key]}}" />
			% elif key == "_id":
				<p>
					{{user[key]}}<b>(Id can not be changed)</b>
				</p>
				<input name="{{ key }}" type="hidden" value="{{user[key]}}" /><!-- Hidden, because we don't want users to modify their ids... But we need to change the email -->
			% else:
				<p> {{user[key]}}</p>
			% end

		</div>
	% end
	
	<input type="submit" value="Send me!">
</form>
