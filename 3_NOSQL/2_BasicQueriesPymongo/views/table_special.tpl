	
	% include('header.tpl')

	<h1 class="title">Results for your query:</h1>
	
	% if len(userList) <= 0:

		<h2 class="subtitle">
			No users found with that parameters values
		</h2> 
	% else:

		<h2 class="subtitle">
			<strong>{{totalResults}}</strong> results found
		</h2>

		<table style="width:100%">
			<tbody>

				<tr>
					<th><p>ID</p></th>
					<th><p>Email</p></th>
				</tr>

				% for user in userList:
				<tr>
					<td><p>{{user['_id']}}</p></td>
					<td><p>{{user['email']}}</p></td> 
				</tr>
				% end
			</tbody>
		</table>

	% end

% include('footer.tpl')