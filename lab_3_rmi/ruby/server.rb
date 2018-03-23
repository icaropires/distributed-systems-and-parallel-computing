require 'drb/drb'

class Operations
	def sum(a, b)
		a + b
	end

	def sub(a, b)
		a - b
	end

	def mult(a, b)
		a * b
	end

	def div(a, b)
		a / b
	end
end

operations = Operations.new

ip, port = ARGV

DRb.start_service("druby://#{ip}:#{port}", operations)
DRb.thread.join
